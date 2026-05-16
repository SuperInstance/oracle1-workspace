"""
Tests for PLATO Training Rooms.
"""

import pytest
import torch
import torch.nn as nn

from plato_training import (
    TrainingTile,
    TileType,
    TileLifecycle,
    LamportClock,
    TrainingConfig,
    AdapterConfig,
    TrainingMetrics,
    TrainingRoom,
    LoRAFactory,
    LoRALayer,
    inject_lora,
)


# ── Type Tests ──────────────────────────────────────────────

class TestTileLifecycle:
    def test_create_tile_is_active(self):
        tile = TrainingTile(name="test", tile_type=TileType.ADAPTER)
        assert tile.state == TileLifecycle.ACTIVE
        assert tile.is_active()
    
    def test_supersede_tile(self):
        old = TrainingTile(tile_id="old", name="v1", tile_type=TileType.ADAPTER)
        new = TrainingTile(tile_id="new", name="v2", tile_type=TileType.ADAPTER)
        result = old.supersede(new)
        assert old.state == TileLifecycle.SUPERSEDED
        assert result.state == TileLifecycle.ACTIVE
        assert result.parent_tile == "old"
        assert not old.is_active()
        assert new.is_active()
    
    def test_retract_tile(self):
        tile = TrainingTile(name="bad", tile_type=TileType.ADAPTER)
        tile.retract("failed evaluation")
        assert tile.state == TileLifecycle.RETRACTED
        assert "RETRACTED" in tile.description
    
    def test_tile_serialization(self):
        tile = TrainingTile(
            tile_id="test-1",
            room="test-room",
            tile_type=TileType.ADAPTER,
            name="test-adapter",
            adapter_config=AdapterConfig(rank=16, alpha=32),
        )
        d = tile.to_dict()
        assert d["tile_type"] == "adapter"
        assert d["state"] == "active"
        
        restored = TrainingTile.from_dict(d)
        assert restored.tile_type == TileType.ADAPTER
        assert restored.adapter_config.rank == 16
    
    def test_tile_summary(self):
        tile = TrainingTile(
            name="spam-detector",
            tile_type=TileType.ADAPTER,
            base_model="gpt2-small",
        )
        summary = tile.summary()
        assert "ADAPTER" in summary
        assert "spam-detector" in summary


class TestLamportClock:
    def test_monotonic(self):
        clock = LamportClock()
        t1 = clock.tick()
        t2 = clock.tick()
        t3 = clock.tick()
        assert t1 < t2 < t3
    
    def test_merge(self):
        clock = LamportClock()
        t1 = clock.tick()  # 1
        t2 = clock.merge(100)  # max(1, 100) + 1 = 101
        assert t2 == 101
    
    def test_now(self):
        clock = LamportClock(time=42)
        assert clock.now() == 42


class TestConfigs:
    def test_adapter_config_defaults(self):
        config = AdapterConfig()
        assert config.rank == 8
        assert config.alpha == 16
        assert config.dropout == 0.0
    
    def test_training_config_defaults(self):
        config = TrainingConfig()
        assert config.learning_rate == 2e-4
        assert config.epochs == 3
        assert config.batch_size == 8


# ── LoRA Tests ──────────────────────────────────────────────

class TestLoRALayer:
    def test_lora_output_matches_original_initially(self):
        """LoRA should produce same output as original layer at init (B=0)."""
        original = nn.Linear(64, 32)
        lora = LoRALayer(original, rank=4, alpha=8)
        
        x = torch.randn(2, 64)
        with torch.no_grad():
            original_out = original(x)
            lora_out = lora(x)
        
        # Should be very close (B initialized to 0)
        assert torch.allclose(original_out, lora_out, atol=1e-6)
    
    def test_lora_has_fewer_trainable_params(self):
        """LoRA should have far fewer parameters than the original."""
        original = nn.Linear(512, 512)
        lora = LoRALayer(original, rank=8)
        
        original_params = 512 * 512  # 262,144
        lora_params = lora.num_trainable_params()  # 512*8 + 8*512 = 8,192
        
        assert lora_params < original_params / 10
        assert lora_params == 512 * 8 + 8 * 512  # 8,192
    
    def test_lora_merge(self):
        """Merging should produce equivalent output."""
        original = nn.Linear(32, 16)
        lora = LoRALayer(original, rank=4, alpha=8)
        
        # Simulate some training
        with torch.no_grad():
            lora.lora_A.normal_(0, 0.01)
            lora.lora_B.normal_(0, 0.01)
        
        x = torch.randn(4, 32)
        with torch.no_grad():
            lora_out = lora(x)
            merged = lora.merge()
            merged_out = merged(x)
        
        assert torch.allclose(lora_out, merged_out, atol=1e-5)


class TestInjectLora:
    def test_inject_into_simple_model(self):
        """LoRA injection should work on a simple model."""
        model = nn.Sequential(
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
        )
        
        # Inject into all Linear layers
        model = inject_lora(model, rank=4, target_modules=["0", "2"])
        
        # Count trainable params
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total = sum(p.numel() for p in model.parameters())
        
        assert trainable > 0
        assert trainable < total  # Most params should be frozen
    
    def test_gpt_model_injection(self):
        """LoRA injection should work on GPT-like architecture."""
        # Simplified GPT model
        class SimpleGPTBlock(nn.Module):
            def __init__(self, d_model=64, n_heads=4):
                super().__init__()
                self.W_query = nn.Linear(d_model, d_model)
                self.W_key = nn.Linear(d_model, d_model)
                self.W_value = nn.Linear(d_model, d_model)
                self.W_out = nn.Linear(d_model, d_model)
                self.ffn = nn.Sequential(
                    nn.Linear(d_model, d_model * 4),
                    nn.GELU(),
                    nn.Linear(d_model * 4, d_model),
                )
            
            def forward(self, x):
                q = self.W_query(x)
                k = self.W_key(x)
                v = self.W_value(x)
                attn = q @ k.transpose(-2, -1) / (x.size(-1) ** 0.5)
                attn = torch.softmax(attn, dim=-1)
                out = attn @ v
                out = self.W_out(out)
                return out + self.ffn(x)
        
        model = SimpleGPTBlock()
        model = inject_lora(model, rank=8, target_modules=["W_query", "W_value"])
        
        # Check that only LoRA params are trainable
        trainable_names = [n for n, p in model.named_parameters() if p.requires_grad]
        assert any("lora_A" in n for n in trainable_names)
        assert any("lora_B" in n for n in trainable_names)
        
        # Forward pass should still work
        x = torch.randn(2, 10, 64)
        out = model(x)
        assert out.shape == (2, 10, 64)


# ── Room Tests ──────────────────────────────────────────────

class TestTrainingRoom:
    def test_create_room(self):
        factory = LoRAFactory("test-room")
        assert factory.room_name == "test-room"
        assert factory.room_type == "lora-factory"
    
    def test_create_tile(self):
        factory = LoRAFactory("test-room")
        tile = factory.create_tile(
            name="test-adapter",
            tile_type=TileType.ADAPTER,
            description="test",
        )
        assert tile.tile_id == "test-room-1"
        assert tile.lamport == 1
        assert tile.is_active()
    
    def test_lifecycle_management(self):
        factory = LoRAFactory("test-room")
        t1 = factory.create_tile("v1", TileType.ADAPTER)
        t2 = factory.create_tile("v2", TileType.ADAPTER)
        
        # Supersede v1 with v2
        result = factory.supersede_tile(t1.tile_id, t2)
        assert result is not None
        
        stats = factory.lifecycle_stats()
        assert stats["active"] == 1
        assert stats["superseded"] == 1
    
    def test_retract(self):
        factory = LoRAFactory("test-room")
        tile = factory.create_tile("bad", TileType.ADAPTER)
        assert factory.retract_tile(tile.tile_id, "failed eval")
        assert tile.state == TileLifecycle.RETRACTED
    
    def test_get_active_tiles(self):
        factory = LoRAFactory("test-room")
        t1 = factory.create_tile("v1", TileType.ADAPTER)
        t2 = factory.create_tile("v2", TileType.ADAPTER)
        t3 = factory.create_tile("metrics", TileType.METRICS)
        
        factory.retract_tile(t2.tile_id, "bad")
        
        active = factory.get_active_tiles()
        assert len(active) == 2
        
        active_adapters = factory.get_active_tiles(TileType.ADAPTER)
        assert len(active_adapters) == 1
    
    def test_room_summary(self):
        factory = LoRAFactory("spam-detector")
        factory.create_tile("v1", TileType.ADAPTER)
        summary = factory.summary()
        assert "lora-factory" in summary
        assert "spam-detector" in summary
    
    def test_predict(self):
        factory = LoRAFactory("spam-detector")
        prediction = factory.predict()
        assert prediction.tile_type == TileType.PREDICTION
        assert prediction.lamport > 0


class TestLoRAFactoryTraining:
    """Test actual LoRA training with a simple model."""
    
    def test_train_simple_classifier(self):
        """Train a LoRA adapter on a simple classification task."""
        # Simple model
        model = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 2),
        )
        
        # Dummy data
        torch.manual_seed(42)
        X = torch.randn(100, 10)
        y = (X[:, 0] > 0).long()  # Simple classification
        
        dataset = torch.utils.data.TensorDataset(X, y)
        train_loader = torch.utils.data.DataLoader(dataset, batch_size=16)
        
        factory = LoRAFactory("test-classifier")
        factory.configure(
            model,
            adapter_config=AdapterConfig(rank=4, alpha=8),
            training_config=TrainingConfig(epochs=2, learning_rate=1e-3),
        )
        
        tile = factory.train(train_loader, num_classes=2)
        
        assert tile.tile_type == TileType.ADAPTER
        assert tile.is_active()
        assert tile.metrics is not None
        assert tile.metrics.epochs_completed == 2
        assert tile.metrics.final_loss > 0
        assert tile.data_path is not None
    
    def test_evaluate_adapter(self):
        """Evaluate a trained adapter tile."""
        model = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 2),
        )
        
        torch.manual_seed(42)
        X = torch.randn(50, 10)
        y = (X[:, 0] > 0).long()
        dataset = torch.utils.data.TensorDataset(X, y)
        loader = torch.utils.data.DataLoader(dataset, batch_size=16)
        
        factory = LoRAFactory("test-eval")
        factory.configure(model, training_config=TrainingConfig(epochs=1))
        tile = factory.train(loader, num_classes=2)
        
        results = factory.evaluate(tile)
        assert "train_loss" in results
        assert "final_loss" in results

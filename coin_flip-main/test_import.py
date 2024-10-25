try:
    from solana.keypair import Keypair
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")

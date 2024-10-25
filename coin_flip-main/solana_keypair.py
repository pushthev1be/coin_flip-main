# Importing necessary modules from the solana library
try:
    # Adjusting the import based on the current structure of the solana package
    from solana.keypair import Keypair  # Update this line if the path has changed
    # If the above line fails, you might want to try the following:
    # from solana import Keypair  # Uncomment this line if the previous line doesn't work

    # Create a new Keypair instance
    keypair = Keypair()

    # Display the public and private keys
    print(f"Public Key: {keypair.public_key}")
    print(f"Secret Key: {keypair.secret}")

    # Optionally, you can save the keypair to a file or use it for further actions
except ImportError as e:
    print(f"Import failed: {e}")

def calculate_pnl():
    try:
        capital = float(input("Enter Capital ($): "))
        leverage = float(input("Enter Leverage (x): "))
        entry_price = float(input("Enter Entry Price: "))
        exit_price = float(input("Enter Exit Price: "))
        position = input("Enter Position (long/short): ").strip().lower()

        position_size = capital * leverage  # Liquidity

        if position == "long":
            pnl = (exit_price - entry_price) / entry_price * position_size
            liquidation_price = entry_price - (entry_price / leverage)
        elif position == "short":
            pnl = (entry_price - exit_price) / entry_price * position_size
            liquidation_price = entry_price + (entry_price / leverage)
        else:
            raise ValueError("Invalid position type. Please enter 'long' or 'short'.")

        pnl_percent = (pnl / capital) * 100

        print("\nResults:")
        print(f"Liquidity (Position Size): ${position_size:.2f}")
        print(f"PnL: ${pnl:.2f}")
        print(f"PnL %: {pnl_percent:.2f}%")
        print(f"Liquidation Price: {liquidation_price:.4f}")

    except ValueError as e:
        print(f"Input Error: {e}")

if __name__ == "__main__":
    calculate_pnl()
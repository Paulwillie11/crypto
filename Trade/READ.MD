# Trade PnL Calculator

A simple command-line Python application to calculate trading profit and loss (PnL), leverage, and liquidation price.

## Features

- Calculates position size (liquidity), PnL in USD and percentage.
- Supports long and short positions.
- Runs in command line, no GUI required.
- Dockerized for easy deployment.

## Requirements

- Docker installed on your machine.

## Usage

### Build Docker Image

From the project root directory (where your Dockerfile and `Trade_cal.py` are located), run:

```bash
docker build -t trade-pnl-calculator .

Run the Application

docker run -it trade-pnl-calculator

You will be prompted to enter:

Capital ($)

Leverage (x)

Entry Price

Exit Price

Position (long/short)


The program will output your position size, PnL, PnL percentage, and liquidation price.

Project Structure

/Trade
  |-- Dockerfile
  |-- Trade_cal.py
  |-- README.md

Notes

Make sure to use lowercase for the Docker image name.

The app runs interactively in the terminal.



### license



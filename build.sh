rm -rf build
rm -rf build-mainnet

SmartPy.sh compile ./contracts/tezrun.py ./build
SmartPy.sh compile ./contracts/tezrun-mainnet.py ./build-mainnet



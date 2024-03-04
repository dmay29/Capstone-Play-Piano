set -e

cd base/playp_base
mkdir -p build
cd build
cmake ../../
make
sudo make install

cd ../../../

cd key_control/playp_key_control
mkdir -p build
cd build
cmake ../../
make
sudo make install

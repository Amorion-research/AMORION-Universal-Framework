#!/usr/bin/env bash
set -e

# Klona mall-repo om det inte finns
if [ ! -d ".amorion-templates" ]; then
  git clone https://github.com/philip/amorion-templates.git .amorion-templates
fi

# Synka mallar
rsync -avr .amorion-templates/ ./

# Gör skript körbara
chmod +x setup_amorion.sh modules/SS1_tensor/pilot_test_A.py experiments/exp1_ss1_tensor.sh

# Kör pilot-test
bash experiments/exp1_ss1_tensor.sh

# Visa resultat
echo "--- Filer i SS1_tensor ---"
ls modules/SS1_tensor

echo "--- Mutual Information ---"
cat modules/SS1_tensor/mutual_information.txt

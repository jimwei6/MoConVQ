bash "./convert_amass_bvh.sh" "../amass_ds/acad/" "./amass_ds/accad"
bash "./convert_amass_bvh.sh" "../amass_ds/BMLhandball/" "./amass_ds/BMLhandball"
bash "./convert_amass_bvh.sh" "../amass_ds/DanceDB/" "./amass_ds/DanceDB"

bash './tracking_directory.sh' './amass_ds/accad/' 'accad' './experiments'
bash './tracking_directory.sh' './amass_ds/BMLhandball/' 'BMLhandball' './experiments'
bash './tracking_directory.sh' './amass_ds/DanceDB/' 'DanceDB' './experiments'

python './Script/recenter_bvh.py' './experiments/accad'
python './Script/recenter_bvh.py' './experiments/BMLhandball'
python './Script/recenter_bvh.py' './experiments/DanceDB'

python './Script/evaluate.py' './amass_ds/accad' './experiments/accad' './accad.json' './accad.csv'
python './Script/evaluate.py' './amass_ds/BMLhandball' './experiments/BMLhandball' './BMLhandball.json' './BMLhandball.csv'
python './Script/evaluate.py' './amass_ds/accad' './experiments/DanceDB' './DanceDB.json' './DanceDB.csv'

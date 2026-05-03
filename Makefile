setup:
	conda env create -f environment.yml
	conda activate proyectofinalbdtools && python -m ipykernel install --user --name proyectofinalbdtools --display-name "Python (proyectofinalbdtools)"

etl:
	python -c "from bdtools.io import run_etl; run_etl()"

eda:
	python -c "from bdtools.io import run_etl; from bdtools.eda import run_eda; df,_=run_etl(); run_eda(df)"

model:
	python -c "from bdtools.io import run_etl; from bdtools.modeling import train_high_impact_classifier, run_spatial_clustering; df,_=run_etl(); train_high_impact_classifier(df); run_spatial_clustering(df)"

flow:
	prefect server start

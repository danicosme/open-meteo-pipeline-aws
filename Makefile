# make -f Makefile all
APP_DIR = app/src
COMMON_DIR = $(APP_DIR)/common
INGESTION_DIR = $(APP_DIR)/ingestion
ENRICHMENT_DIR = $(APP_DIR)/enrichment
PROCESSING_DIR = $(APP_DIR)/processing
OUTPUT_DIR = dist

.PHONY: all clean create_dist_dir ingestion_zip enrichment_zip processing_zip

all: clean create_dist_dir ingestion_zip enrichment_zip processing_zip

clean:
	rm -rf $(OUTPUT_DIR)

create_dist_dir:
	mkdir -p $(OUTPUT_DIR)

ingestion_zip: create_dist_dir
	mkdir -p $(OUTPUT_DIR)/temp_ingestion
	mkdir -p $(OUTPUT_DIR)/temp_ingestion/common
	cp -r $(COMMON_DIR)/* $(OUTPUT_DIR)/temp_ingestion/common/
	cp -r $(INGESTION_DIR)/* $(OUTPUT_DIR)/temp_ingestion/
	cd $(OUTPUT_DIR)/temp_ingestion && zip -r ../ingestion.zip ./*
	rm -rf $(OUTPUT_DIR)/temp_ingestion

processing_zip: create_dist_dir
	mkdir -p $(OUTPUT_DIR)/temp_processing
	mkdir -p $(OUTPUT_DIR)/temp_processing/common
	cp -r $(COMMON_DIR)/* $(OUTPUT_DIR)/temp_processing/common/
	cp -r $(PROCESSING_DIR)/* $(OUTPUT_DIR)/temp_processing/
	cd $(OUTPUT_DIR)/temp_processing && zip -r ../processing.zip ./*
	rm -rf $(OUTPUT_DIR)/temp_processing

enrichment_zip: create_dist_dir
	mkdir -p $(OUTPUT_DIR)/temp_enrichment
	mkdir -p $(OUTPUT_DIR)/temp_enrichment/common
	cp -r $(COMMON_DIR)/* $(OUTPUT_DIR)/temp_enrichment/common/
	cp -r $(ENRICHMENT_DIR)/* $(OUTPUT_DIR)/temp_enrichment/
	cd $(OUTPUT_DIR)/temp_enrichment && zip -r ../enrichment.zip ./*
	rm -rf $(OUTPUT_DIR)/temp_enrichment



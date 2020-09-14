library(Seurat)

# Read in results and convert cells to rownames
results <- read.csv("results/final_types.csv")
rownames(results) <- results[["cell"]]
results <- results["predicted.id"]

# Add predicted.id and print head
obj <- readRDS("data/query.rds")
obj <- AddMetaData(obj, metadata = results)
Idents(obj) <- "predicted.id"

head(Idents(obj))

# And save!
saveRDS(obj, "data/query.rds")

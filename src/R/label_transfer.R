library(Matrix)
library(Seurat)

out_path <- file.path("results")

# Create if out_path doesn't exist
if (!dir.exists(out_path)) {
  dir.create(out_path)
}

# Coarse cell types tier
# Data not provided in repository
message("Coarse label transfer")
message("\tReading data...")

reference <- readRDS(file.path("data", "reference.rds"))
message("\tReference data:")
print(reference)
query <- readRDS(file.path("data", "query.rds"))
message("\tQuery data:")
print(query)

Idents(reference) <- "final_coarse_clusters"

message("\tLearning anchors...")
anchors <- FindTransferAnchors(
  reference = reference,
  query = query,
  normalization.method = "LogNormalize",
  reference.assay = "integrated",
  query.assay = "RNA",
  reduction = "pcaproject",
  features = VariableFeatures(object = reference),
  npcs = NULL,
  dims = 1:28
)
message("\tTransferring labels...")
predictions <- TransferData(
  anchorset = anchors,
  refdata = reference$final_coarse_clusters,
  weight.reduction = "pcaproject",
  dims = 1:28
)
query <- AddMetaData(query, metadata = predictions)

# Save queried results
message("\tSaving coarse results...")
coarse_type <- query[["predicted.id"]]
write.csv(
  coarse_type,
  file = file.path(out_path, "coarse_types.csv"),
  row.names = T
)

# Save counts, features, and labels for Neural Network
query_neural <- subset(
  query,
  subset = predicted.id %in% c("Neuron", "Doublets", "Motorneuron")
)

counts <- GetAssayData(query_neural, assay = "RNA", slot = "counts")
counts <- t(counts)
writeMM(obj = counts, file = file.path(out_path, "query_neural_counts.mtx"))

features <- rownames(query_neural$RNA)
write.csv(
  features,
  file = file.path(out_path, "query_neural_features.csv"),
  row.names = F
)

cells <- colnames(query_neural$RNA)
write.csv(
  cells,
  file = file.path(out_path, "query_neural_cells.csv"),
  row.names = F
)

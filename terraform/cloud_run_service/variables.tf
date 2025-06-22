variable "project_id" {
  type        = string
  description = "Name of the Google Project"
}

variable "region" {
  type        = string
  default     = "europe-west2"
  description = "Location for the resources"
}

variable "image_name" {
  type        = string
  description = "Docker image name"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag"
}

variable "repo_name" {
  type        = string
  description = "Artifact registry repository name"
}

variable "service_account_id" {
  type        = string
  description = "Service account ID to be used by Cloud Run service"
}

variable "service_name" {
  type        = string
  description = "Name of the Cloud Run service"
}

dir <- getwd()
setwd(dir)

# install.packages("rjson", dependencies=TRUE, repos = "https://cran.rstudio.com/")

library(rjson)

json_file = "reviews_Home_and_kitchenSHORT.json"

json_data <- fromJSON(paste(readLines(json_file), collapse=""))



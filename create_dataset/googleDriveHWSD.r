library(raster)
library(sp)
library(dplyr)

path <- "/content/drive/MyDrive/SOCData/hwsd.bil"

hwsd <- raster(path)
print(hwsd)
proj4string(hwsd) <-  "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"

args <- commandArgs(trailingOnly = TRUE)

START_LONG = as.numeric(args[1])
END_LONG = as.numeric(args[2])
START_LAT = as.numeric(args[3])
END_LAT = as.numeric(args[4])

cat(START_LAT)
cat(END_LAT)

hwsd.sample <- crop(hwsd, extent(c(START_LONG, END_LONG, END_LAT, START_LAT)))

# metadata / other info
print(hwsd.sample)

MU.GLOBAL.IDS <- list()
long1 <- list()
long2 <- list()
lat1 <- list()
lat2 <- list()

xFromColLists <- list()
yFromRowLists <- list()

for (i in 1:240) {
	xFromColLists[[i]] <- xFromCol(hwsd.sample, i)
	yFromRowLists[[i]] <- yFromRow(hwsd.sample, i)
}

# print(xFromColLists)

numRows <- 0

for (i in 1:239) {
	for (j in 1:239) {
		block <- getValuesBlock(hwsd.sample, row = i, nrows=1, col = j, ncols = 1)
		if (block != 0) {
			numRows <- numRows + 1
			MU.GLOBAL.IDS[[numRows]] <- block
			if (j > 1) {
				long1[[numRows]] <- (xFromColLists[[j - 1]] + xFromColLists[[j]]) / 2
			} else {
				long1[[numRows]] <- START_LONG
			}
			long2[[numRows]] <- (xFromColLists[[j]] + xFromColLists[[j + 1]]) / 2
			if (i > 1) {
				lat1[[numRows]] <- (yFromRowLists[[i - 1]] + yFromRowLists[[i]]) / 2
			} else {
				lat1[[numRows]] <- START_LAT
			}
			lat2[[numRows]] <- (yFromRowLists[[i]] + yFromRowLists[[i + 1]]) / 2
		}
	}
	print(i)
}

df <- data.frame(
	I(MU.GLOBAL.IDS),
	I(long1),
	I(long2),
	I(lat2),
	I(lat1)
)

# df <- sample_n(df, size = 200, replace = FALSE)

names(df) <- c('MU_GLOBAL', 'LONG1', 'LONG2', 'LAT1', 'LAT2')
write.table(df, "/content/drive/MyDrive/SOCData/latdata.csv", sep=",", row.names = FALSE, col.names = FALSE, append=TRUE)
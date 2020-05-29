REM GoodParallel: FfmpegParallelTest

REM Scale, make palette, then scale and convert to GIF (this looks really bad)
REM ffmpeg -i %1 -an -filter_complex "[0:v]scale='960:-2'[scaled]; [scaled] palettegen" palette.png
REM ffmpeg -i %1 -i palette.png -filter_complex "[0:v]scale='960:-2'[scaled]; [scaled][1:v] paletteuse" %2

REM Make palette, then convert to GIF (this looks really good, but two commands is silly)
REM ffmpeg -y -i %1 -an -filter_complex "[0:v] palettegen" palette.png
REM ffmpeg -y -i %1 -i palette.png -filter_complex "[0:v][1:v] paletteuse" %2

REM Make palette and convert to GIF in one step
ffmpeg -y -i %1 -an -filter_complex "[0:v] palettegen [palette]; [0:v][palette] paletteuse" %2

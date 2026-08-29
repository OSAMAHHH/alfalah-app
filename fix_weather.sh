sed -i 's/http:\/\/ip-api.com\/json/https:\/\/ipwho.is\//g' app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt
sed -i 's/"lat",/"latitude",/g' app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt
sed -i 's/"lon",/"longitude",/g' app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt

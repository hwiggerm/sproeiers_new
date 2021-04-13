<?php
/* Connect to the MySQL database */
$data_base = mysqli_connect('localhost', 'meteo', 'regendruppel','weather');

/* Get data from mysql */
$sql = 'select * from weerinfo';

$temperatures = mysqli_query($data_base, $sql);

echo "Today is " . date("Y-m-d") . "<br>";
echo "<br>";
echo "<H1>Summary and settings</H1>";
echo "<br>";

echo "<head>";
echo "<style>";
echo "table, td, th {";
echo "  border: 1px solid black;";
echo "}";
echo "table {";
echo "  width: 100%;";
echo "  border-collapse: collapse;";
echo "}";
echo "</style>";
echo "</head>";
echo "<table>";
echo "<tr>";
echo "<td>Timestamp";
echo "<td>Yesterday Temperature";
echo "<td>Yesterday Humidity";
echo "<td>Yesterday Rain";
echo "<td>Todays Temperature";
echo "<td>Todays Humidity";
echo "<td>Todays Rainfall";
echo "<td>Sproeitijd ";
echo "<td>Sunrise";
echo "<tr>";

while ($temperature_row = mysqli_fetch_array($temperatures))
{
  echo "<tr>";
  echo "<td>".$temperature_row["timestamp"];

  echo "<td>".$temperature_row["ytemp"];
  echo "<td>".$temperature_row["yhum"];
  echo "<td>".$temperature_row["yrain"];

  echo "<td>".$temperature_row["ttemp"];
  echo "<td>".$temperature_row["thum"];
  echo "<td>".$temperature_row["train"];

  echo "<td>".$temperature_row["sproeitijd"];
  echo "<td>".$temperature_row["sunrise"];


  echo "<tr>";
}


echo "<tr>";
echo "</table>";

echo "<hr>";

echo "<br>";
echo "<H1>Today's Data</H1>";
echo "<br>";

$sql = "select * from logweather where logdate like '" . date("Y-m-d")."%'" ;
$temperatures = mysqli_query($data_base, $sql);


echo "<table>";
echo "<tr>";
echo "<td>Logdate";
echo "<td>Temp Inside";
echo "<td>Temp Outside";
echo "<td>Weather";
echo "<td>humidity";
echo "<td>Rain next hour";
echo "<tr>";

while ($temperature_row = mysqli_fetch_array($temperatures))
{
  echo "<tr>";  echo "<td>".$temperature_row["logdate"];
  echo "<td>".$temperature_row["tempin"];
  echo "<td>".$temperature_row["tempout"];
  echo "<td>".$temperature_row["weather"];
  echo "<td>".$temperature_row["humidity"];
  echo "<td>".$temperature_row["rain 1H"];
  echo "<tr>";
}


echo "<tr>";
echo "</table>";

echo "<hr>" ;

echo "<br>";
echo "<H1>Actions Today</H1>";
echo "<br>";



$file = file("/home/pi/sprinkler.log");
for ($i = max(0, count($file)-24); $i < count($file); $i++) {
  echo $file[$i] . "<br>";
}


?>

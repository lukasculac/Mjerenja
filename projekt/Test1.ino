#include <Wire.h>
#include <ClosedCube_OPT3001.h>
#include <Adafruit_DPS310.h>
#include <HDC2010.h>

#define OPT3001_ADDRESS 0x44
#define HDC_ADDRESS 0x40
#define DPS_ADDRESS 0x77

ClosedCube_OPT3001 opt3001;
HDC2010 hdc(HDC_ADDRESS); 
Adafruit_DPS310 dps;
Adafruit_Sensor *dps_temp = dps.getTemperatureSensor();
Adafruit_Sensor *dps_pressure = dps.getPressureSensor();


float humidity = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  hdc.begin();
  hdc.reset();

  opt3001.begin(OPT3001_ADDRESS);
  
  dps.begin_I2C(DPS_ADDRESS);
  configureSensor();
  
  // Setup highest precision
  dps.configurePressure(DPS310_64HZ, DPS310_64SAMPLES);
  dps.configureTemperature(DPS310_64HZ, DPS310_64SAMPLES);

  //hdc.setHighTemp(28);         // High temperature of 28C
  //hdc.setLowTemp(22);          // Low temperature of 22C
  hdc.setHighHumidity(55);     // High humidity of 55%
  hdc.setLowHumidity(40);      // Low humidity of 40%
  
  // Configure Measurements
  hdc.setMeasurementMode(HUMID_ONLY);  // Set measurements to temperature and humidity
  hdc.setRate(ONE_HZ);                     // Set measurement frequency to 1 Hz
  hdc.setTempRes(FOURTEEN_BIT);
  hdc.setHumidRes(FOURTEEN_BIT);
  
  //begin measuring
  hdc.triggerMeasurement();
}

void loop() {
  //DPS code
  sensors_event_t temp_event, pressure_event;
  
  if (dps.temperatureAvailable()) {
    dps_temp->getEvent(&temp_event);
    //Serial.print(F("Temperature = "));
    Serial.print(temp_event.temperature);
    Serial.print("x");
    //Serial.println(" *C");
  }
  
    dps_pressure->getEvent(&pressure_event);
    //Serial.print(F("Pressure = "));
    Serial.print(pressure_event.pressure);
    Serial.print("x");
    //Serial.println(" hPa"); 
 
  //OPT code
  OPT3001 result = opt3001.readResult();
  printResult("OPT3001", result);
  Serial.print("x");

  //HDC code
  humidity = hdc.readHumidity();
  //Serial.print("%RH: ");
  Serial.print(humidity);
  
  Serial.println();
  delay(1000);
  
}

void configureSensor() {
  OPT3001_Config newConfig;
  
  newConfig.RangeNumber = B1100;  
  newConfig.ConvertionTime = B0;
  newConfig.Latch = B1;
  newConfig.ModeOfConversionOperation = B11;

  OPT3001_ErrorCode errorConfig = opt3001.writeConfig(newConfig);
  if (errorConfig != NO_ERROR)
    printError("OPT3001 configuration", errorConfig);
  else {
    OPT3001_Config sensorConfig = opt3001.readConfig();
  }
  
}

void printResult(String text, OPT3001 result) {
  if (result.error == NO_ERROR) {
    //Serial.print(text);
    //Serial.print(": ");
    Serial.print(result.lux);
   // Serial.println(" lux");
  }
  else {
    printError(text,result.error);
  }
}

void printError(String text, OPT3001_ErrorCode error) {
  Serial.print(text);
  Serial.print(": [ERROR] Code #");
  Serial.println(error);
}

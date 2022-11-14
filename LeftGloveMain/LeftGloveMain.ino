#include <ArduinoBLE.h>
#include <PDM.h>
#include <Arduino_LSM9DS1.h>

// This device's MAC:
// C8:5C:A2:2B:61:86
//#define LEDR        (23u)
//#define LEDG        (22u)
//#define LEDB        (24u)

// Device name
const char* nameOfPeripheral = "Arduino Nano BLE 33";
const char* uuidOfService = "00001101-0000-1000-8000-00805f9b34fb";
const char* uuidOfRxChar = "00001144-0000-1000-8000-00805f9b34fb";
const char* uuidOfTxChar = "00001145-0000-1000-8000-00805f9b34fb";

// BLE Service
BLEService microphoneService(uuidOfService);

// Setup the incoming data characteristic (RX).
const int WRITE_BUFFER_SIZE = 256;
bool WRITE_BUFFER_FIZED_LENGTH = false;

// RX / TX Characteristics
BLECharacteristic rxChar(uuidOfRxChar, BLEWriteWithoutResponse | BLEWrite, WRITE_BUFFER_SIZE, WRITE_BUFFER_FIZED_LENGTH);
BLEByteCharacteristic txChar(uuidOfTxChar, BLERead | BLENotify | BLEBroadcast);

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[256];

// Number of samples read
volatile int samplesRead;

// IMU variables
float Ax, Ay, Az;
float Gx, Gy, Gz;
int degreesX = 0;
int degreesY = 0;
int fc = 0, bc = 0, rc = 0, lc = 0; // gesture recognition counters
int gestureMinLength = 15;
int plusThreshold = 230, minusThreshold = -230;

typedef union {
	struct {
		float x;
		float y;
		float z;
	} sample;
	uint8_t bytes[12];
} IMU_Sample;

// send string over BLE
typedef union {
	struct {
		char chars[12];
	} chars;
	uint8_t bytes[12];
} Chars;


/*
 *  MAIN
 */
void setup() {

  // Start serial.
  // Serial.begin(9600);

  // Ensure serial port is ready.
  // while (!Serial);
  //serialLight();

  // Prepare LED pins.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  // Configure the data receive callback
  // PDM.onReceive(onPDMdata);

  // Start PDM
  startPDM();

  // Start IMU
  startIMU();

  // Start BLE.
  startBLE();

  // Create BLE service and characteristics.
  //BLE.setLocalName(nameOfPeripheral);
  BLE.setAdvertisedService(microphoneService);
  microphoneService.addCharacteristic(rxChar);
  microphoneService.addCharacteristic(txChar);
  BLE.addService(microphoneService);

  // Bluetooth LE connection handlers.
  BLE.setEventHandler(BLEConnected, onBLEConnected);
  BLE.setEventHandler(BLEDisconnected, onBLEDisconnected);
  
  // Event driven reads.
  rxChar.setEventHandler(BLEWritten, onRxCharValueUpdate);
  
  // Let's tell devices about us.
  BLE.setLocalName("LeftGlove");
  BLE.setDeviceName("LeftGlove");
  BLE.advertise();
  
  // Print out full UUID and MAC address.
  //Serial.println("Peripheral advertising info: ");
  //Serial.print("Name: ");
  //Serial.println(nameOfPeripheral);
  //Serial.print("MAC: ");
  //Serial.println(BLE.address());
  //Serial.print("Service UUID: ");
  //Serial.println(microphoneService.uuid());
  //Serial.print("rxCharacteristic UUID: ");
  //Serial.println(uuidOfRxChar);
  //Serial.print("txCharacteristics UUID: ");
  //Serial.println(uuidOfTxChar);


  //Serial.println("Bluetooth device active, waiting for connections...");
}


void loop()
{
  BLEDevice central = BLE.central();

  if (central)
  {
    // Only send data if we are connected to a central device.
    while (central.connected()) {
      connectedLight();
      if (samplesRead == 0 && IMU.accelerationAvailable() == 1 && IMU.gyroscopeAvailable() == 1) {
        onIMUdata();
      }

      // Send the microphone values to the central device.
      if (samplesRead > 0) {
        // print samples to the serial monitor or plotter
        for (int i = 0; i < samplesRead; i++) {
          txChar.writeValue(sampleBuffer[i]);      
        }
        // Clear the read count
        samplesRead = 0;
      }
    }
  } else {
    disconnectedLight();
  }
}


/*
 *  BLUETOOTH
 */
void startBLE() {
  if (!BLE.begin())
  {
    //Serial.println("starting BLE failed!");
    while (1);
  }
}

void onRxCharValueUpdate(BLEDevice central, BLECharacteristic characteristic) {
  // central wrote new value to characteristic, update LED
  //Serial.print("Characteristic event, read: ");
  byte test[256];
  int dataLength = rxChar.readValue(test, 256); // THIS IS WHERE WE GET COMMUNICATION FROM PYTHON

  //for(int i = 0; i < dataLength; i++) {
  //  Serial.print((char)test[i]);
  //}
  //Serial.println();
  //Serial.print("Value length = ");
  //Serial.println(rxChar.valueLength());
}

void onBLEConnected(BLEDevice central) {
  //Serial.print("Connected event, central: ");
  //Serial.println(central.address());
  connectedLight();
}

void onBLEDisconnected(BLEDevice central) {
  //Serial.print("Disconnected event, central: ");
  //Serial.println(central.address());
  disconnectedLight();
}


/*
 *  MICROPHONE
 */
void startPDM() {
  // initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate
  if (!PDM.begin(1, 16000)) {
    //Serial.println("Failed to start PDM!");
    while (1);
  }
}


void onPDMdata() {
  // // query the number of bytes available
  // int bytesAvailable = PDM.available();

  // // read into the sample buffer
  // PDM.read(sampleBuffer, bytesAvailable);

  // // 16-bit, 2 bytes per sample
  // samplesRead = bytesAvailable / 2;
}


/*
 * IMU
 */
void startIMU() {
    // Ensure IMU is ready
  if (!IMU.begin()) {
    //Serial.println("Failed to initialize IMU!");
    while (1);
  }
  //Serial.print("Accelerometer sample rate = ");
  //Serial.print(IMU.accelerationSampleRate());
  //Serial.println("Hz");
}

void onIMUdata() {
  // read into the sample buffer
  IMU.readGyroscope(Gx, Gy, Gz);
  IMU.readAcceleration(Ax, Ay, Az);

  //Serial.println("Gx " + String(Gx));
  //Serial.println("Gy " + String(Gy));
  //Serial.println("Gz " + String(Gz));

  // Create samples
  IMU_Sample gyroSample;
  gyroSample.sample.x = Gx;
  gyroSample.sample.y = Gy;
  gyroSample.sample.z = Gz;

  IMU_Sample accelSample;
  accelSample.sample.x = Ax;
  accelSample.sample.y = Ay;
  accelSample.sample.z = Az;

  // WRITE SAMPLES INTO SAMPLE BUFFER SOMEHOW
  // gyroSample.bytes[0-11]
  // accelSample.bytes[0-11]
  
  // uint8_t sampleBufferBuilder[256];
  // sampleBufferBuilder[0] = '8';
  // sampleBufferBuilder[13] = 'c';
  // for (int i = 0; i < 24; i++) {
  //   if (i < 12) {
  //     sampleBufferBuilder[i + 1] = gyroSample.bytes[i];
  //   } else {
  //     sampleBufferBuilder[i + 2] = accelSample.bytes[i - 12];
  //   }
  // }

  if (Ax > 0.1) {
    Ax = 100 * Ax;
    degreesX = map(Ax, 0, 97, 0, 90);
    //Serial.print("Tilting up ");
    //Serial.print(degreesX);
    //Serial.println("  degrees");
  }
  if (Ax < -0.1) {
    Ax = 100 * Ax;
    degreesX = map(Ax, 0, -100, 0, 90);
    //Serial.print("Tilting down ");
    //Serial.print(degreesX);
    //Serial.println("  degrees");
  }
  if (Ay > 0.1) {
    Ay = 100 * Ay;
    degreesY = map(Ay, 0, 97, 0, 90);
    //Serial.print("Tilting left ");
    //Serial.print(degreesY);
    //Serial.println("  degrees");
  }
  if (Ay < -0.1) {
    Ay = 100 * Ay;
    degreesY = map(Ay, 0, -100, 0, 90);
    //Serial.print("Tilting right ");
    //Serial.print(degreesY);
    //Serial.println("  degrees");
  }

  // Ay *= 100; Ax *= 100;
  degreesX = map(Ax, -100, 97, 0, 90);
  degreesY = map(Ay, -100, 97, 0, 90);

  int tempSamples = 0;
  // [sensorMode][L/R][X/Y][d1][d2][d3][d4][d5]
  sampleBuffer[0] = (uint8_t) (0b10000000 + map(degreesX, 0, 90, 0, 0b11111));
  sampleBuffer[1] = (uint8_t) (0b10100000 + map(degreesY, 0, 90, 0, 0b11111));

  tempSamples += 2;

  if(Gy > plusThreshold)
  {
    //Serial.println("Collision front");
    fc++;
  }
  if(Gy < minusThreshold)
  {
    //Serial.println("Collision back");
    bc++;
  }
  if(Gx < minusThreshold)
  {
    //Serial.println("Collision right");
    rc++;
  }
    if(Gx > plusThreshold)
  {
    //Serial.println("Collision left");
    lc++;    
  }

  int numGestInc = 0;
  if (fc > 2) {
    numGestInc++;
  }
  if (bc > 2) {
    numGestInc++;
  }
  if (rc > 2) {
    numGestInc++;
  }
  if (lc > 2) {
    numGestInc++;
  }
  if (numGestInc > 1) {
    lc = 0;
    rc = 0;
    fc = 0;
    bc = 0;
  }

  // [sensorMode][L/R][X/Y][d1][d2][d3][d4][d5]
  // data --> left = 2, right = 1, front = 3, back = 0
  if (lc >= gestureMinLength) {
    lc = 0;
    sampleBuffer[tempSamples] = (uint8_t) (0b00000010);
    tempSamples++;
  }
  if (rc >= gestureMinLength) {
    rc = 0;
    sampleBuffer[tempSamples] = (uint8_t) (0b00000001);
    tempSamples++;
  }
  if (fc >= gestureMinLength) {
    fc = 0;
    sampleBuffer[tempSamples] = (uint8_t) (0b00000011);
    tempSamples++;
  }
  if (bc >= gestureMinLength) {
    bc = 0;
    sampleBuffer[tempSamples] = (uint8_t) (0b00000000);
    tempSamples++;
  }

  samplesRead = tempSamples;
}


/*
 * LEDS
 */
void connectedLight() {
  digitalWrite(LEDR, LOW);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, LOW);
}

void serialLight() {
  digitalWrite(LEDR, LOW);
  digitalWrite(LEDG, LOW);
  digitalWrite(LEDB, HIGH);
}


void disconnectedLight() {
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, LOW);
  digitalWrite(LEDB, LOW);
}
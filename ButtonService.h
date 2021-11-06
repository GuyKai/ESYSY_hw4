/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef __BLE_BUTTON_SERVICE_H__
#define __BLE_BUTTON_SERVICE_H__

#include "ble/BLE.h"
#include <string>

class ButtonService {
public:
    const static uint16_t BUTTON_SERVICE_UUID              = 0xA000;
    const static uint16_t BUTTON_STATE_CHARACTERISTIC_UUID = 0xA001;
    const static uint16_t ID_CHARACTERISTIC_UUID           = 0xA002;
    const static uint16_t LED_CHARACTERISTIC_UUID          = 0xA003;

    ButtonService(BLE &_ble, bool buttonPressedInitial,bool ledInitial, uint8_t IDnumber[9]) :
        ble(_ble), 
        buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressedInitial, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        IDstate(ID_CHARACTERISTIC_UUID, IDnumber, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        ledState(LED_CHARACTERISTIC_UUID, &ledInitial)
    {
        GattCharacteristic *charTable[] = {&buttonState, &IDstate, &ledState};
        GattService         buttonService(ButtonService::BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
        ble.gattServer().addService(buttonService);
        //uint8_t IDnumber2[9] = {'a', '0', '8', '9', '0', '1', '9', '9', '9'};
        //ble.gattServer().write(IDstate.getValueHandle(), IDnumber2, sizeof(uint8_t)*9);
    }

    void updateButtonState(bool newState) {
        ble.gattServer().write(buttonState.getValueHandle(), (uint8_t *)&newState, sizeof(bool));
    }
    
    void updateIDstate(uint8_t IDnumber[9]) {
        ble.gattServer().write(IDstate.getValueHandle(), IDnumber, 9);
    }

    GattAttribute::Handle_t getValueHandle() const
    {
        return ledState.getValueHandle();
    }

private:
    BLE                              &ble;
    ReadOnlyGattCharacteristic<bool>  buttonState;
    ReadWriteGattCharacteristic<bool>  ledState;
    ReadOnlyArrayGattCharacteristic<uint8_t,9>  IDstate;
};



#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */

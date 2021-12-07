import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';

import QuestionJ from './components/QuestionJ';
import RoomScreen from './components/RoomScreen';


import * as firebase from 'firebase';
import {firebaseConfig} from './config';
import { LogBox } from 'react-native';

LogBox.ignoreLogs(['Setting a timer']);

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
} else {
  firebase.app(); // if already initialized, use that one
}


const MainStack = createStackNavigator();









export default function App() {
  return (
    <NavigationContainer>
      <MainStack.Navigator>
        <MainStack.Screen name="QuestionJ" component={QuestionJ} options={{headerShown: false}}/>
        <MainStack.Screen name="RoomScreen" component={RoomScreen} options={{headerShown: false}}/>
      </MainStack.Navigator>
    </NavigationContainer>

  );
}

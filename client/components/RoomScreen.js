import React, { useState } from 'react';
import { GiftedChat } from 'react-native-gifted-chat';
import {Text, View, Image, FlatList, SafeAreaView, TouchableOpacity, StyleSheet, ScrollView, Alert} from 'react-native';
import * as firebase from 'firebase';
import styles from './Styles';
import { useFocusEffect } from '@react-navigation/native';

export default function RoomScreen(props) {
  // const [messages, setMessages] = useState([
  //   /**
  //    * Mock message data
  //    */
  //   // example of system message
  //   {
  //     _id: 0,
  //     text: 'New room created.',
  //     createdAt: new Date().getTime(),
  //     system: true
  //   },
  //   // example of chat message
  //   {
  //     _id: 1,
  //     text: 'Henlo!',
  //     createdAt: new Date().getTime(),
  //     user: {
  //       _id: 2,
  //       name: 'Test User'
  //     }
  //   }
  // ]);

  const [messages, setMessages] = useState([]);

  


  const messagesRef = firebase.database().ref().child('messages')


  useFocusEffect(
    React.useCallback(() => {
        messagesRef.once('value', function(snapshot) {
           

            var mList= []
            snapshot.forEach(function(childSnapshot) {
               
                const keyOf = childSnapshot.key;
                var childRef = childSnapshot.val()[0];
                
                
                var childData = childRef["text"];
                var id1 = childRef["_id"]
                var id2 = childRef["user"]["_id"]
                var sendName = childRef["user"]["name"]

                console.log(id1);
                console.log(childData)
                console.log(id2)
                console.log(sendName)
  
                var obj = {
                  _id: [id1],
                      text: [childData],
                      createdAt: new Date().getTime(),
                      user: {
                        _id: [id2],
                        name: 'TestUser'
                  }
                }
                mList.push(obj);

                setMessages(mList.reverse());

               

            
                
                
              });
        });
    }, [])
  );

  // helper method that is sends a message
  function handleSend(newMessage = []) {
    console.log(newMessage);
    // newMessage[0]["created"] = new Date().getTime()
    
    setMessages(GiftedChat.append(messages, newMessage));
    console.log(messages);
    messagesRef.push(newMessage);
    
  }

  function backToQuestion() {
        
    props.navigation.navigate('QuestionJ')

    
    
    // loadData();
    
}

  return (
    <View style={styles.container}>
    <GiftedChat
      messages={messages}
      onSend={newMessage => handleSend(newMessage)}
      user={{ _id: 1 }}
    />
    <TouchableOpacity
            style={styles.button4}
            onPress={() => backToQuestion()}
            >
            

            <Text >
                Go Back to Questions</Text>
                    
    </TouchableOpacity>
    </View>
  );
}
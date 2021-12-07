
import React, {useState} from 'react';
import {Text, View, Image, FlatList, SafeAreaView, TouchableOpacity, StyleSheet, ActivityIndicator} from 'react-native';
import * as firebase from 'firebase';
import styles from './Styles';
import { Table, Row, } from 'react-native-table-component';
import axios from 'axios';
import { Dimensions } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';


export default function QuestionJ(props) {
        
    const titleHead = ['SEASON', 'TEAM', 'POS']
    const table1head = ['PTS', 'AST', 'TRB', 'STL']
    const table2head = ['BLK', 'G', 'MP', 'FG%']



    const questionRespRef = firebase.database().ref().child('questionResponses')

    const questionRef = firebase.database().ref().child('questions')


 

    const [playerNames, setPlayerNames] = useState([]);
    const [playerUris, setPlayerUris] = useState([])


    const [p1title, setp1Title1] = useState([]);
    const [p1row1, setp1Row1] = useState([]);
    const [p1row2, setp1Row2] = useState([]);

    const [p2title, setp2Title1] = useState([]);
    const [p2row1, setp2Row1] = useState([]);
    const [p2row2, setp2Row2] = useState([]);
    const [qKey, setQKey] = useState("")


    const baseUrl = 'http://10.0.2.2:5000'





    const loadData = async () => {
        axios.get(baseUrl + '/stats/random')
            .then(function (response) {

                console.log(response);
                
                const data = response.data;
                
                

                
                const p1 = data["player1"]
                const p2 = data["player2"]

                const p1Stats = p1["stats"]
                const p2Stats = p2["stats"]


                setPlayerNames([p1Stats["NAME"], p2Stats["NAME"]])
                console.log(playerNames);
                setPlayerUris([p1["img"], p2["img"]])

                setp1Title1([p1Stats["SEASON"], p1Stats["TEAM"], p1Stats["POS"]])
                setp1Row1([p1Stats["PTS"], p1Stats["AST"], p1Stats["TRB"], p1Stats["STL"]])
                setp1Row2([p1Stats["BLK"], p1Stats["G"], p1Stats["MP"], p1Stats["FG%"]])

                setp2Title1([p2Stats["SEASON"], p2Stats["TEAM"], p2Stats["POS"]])
                setp2Row1([p2Stats["PTS"], p2Stats["AST"], p2Stats["TRB"], p2Stats["STL"]])
                setp2Row2([p2Stats["BLK"], p2Stats["G"], p2Stats["MP"], p2Stats["FG%"]])
                console.log(response)

                
                var fName = p1Stats["NAME"]
                var y1 = p1Stats["SEASON"]
                var sName = p2Stats["NAME"]
                var y2 = p2Stats["SEASON"]
                console.log(fName);
                console.log(sName);
                if (fName.localeCompare(sName) > 0) {
                    fName = p2Stats["NAME"]
                    y1 = p2Stats["SEASON"]
                    sName = p1Stats["NAME"]
                    y2 = p1Stats["SEASON"]
                }
                var qKeyP = fName + y1 + sName + y2
                qKeyP = qKeyP.replace(/\s/g, '');
                console.log(qKeyP);
                console.log(qKeyP)
                setQKey(qKeyP)
                qKeyN = qKeyP
                var respData = 
                {
                    [fName]: 0,
                    [sName]: 0
                }

                var questionData = 
                {
                    player1: {
                        name: [fName][0],
                        season: [y1][0]
                    },
                    player2: {
                        name: [sName][0],
                        season: [y2][0]
                    }
                }
                
                questionRef.once('value', function(snapshot) {
                    if (!snapshot.hasChild(qKeyN)) {
                        questionRespRef.child(qKeyN).set(respData)
                        questionRef.child(qKeyN).set(questionData)
                    }
                });
                


            })
            .catch(function (error) {          
                console.log(error.message);
                throw error;   
            });
    };

    function clearNames() {

        setPlayerNames([])
        setPlayerUris([])

        setp1Title1([])
        setp1Row1([])
        setp1Row2([])

        setp2Title1([])
        setp2Row1([])
        setp2Row2([])
        setQKey("")
    }


    function dataPress(name) {
        console.log(qKey);
        questionRespRef.child(qKey).child(name).once('value').then(function(snapshot) {
            console.log(snapshot.val());
            const valUpdate = snapshot.val();
            console.log(valUpdate);
            questionRespRef.child(qKey).child(name).set(valUpdate + 1);
            
        }).then( () => {
            clearNames();
            props.navigation.navigate('RoomScreen');
        });
        // loadData();
        
    }




    useFocusEffect(
        React.useCallback(() => {
            loadData();
        }, [])
      );
    

   

    const customStyles = StyleSheet.create({
        container: { flex: 1, padding: 16, paddingTop: 30, backgroundColor: '#fff' },
        head: { height: 40, backgroundColor: '#f1f8ff' },
        text: { margin: 6 },
        tableTop: { marginTop: 80, marginBottom: 5}
    });


   

    return (
      //SafeAreaView is used to make the flatlist take up the full screen. Only necessary for iOS devices on iOS versions 11+
      
      
      <SafeAreaView style={styles.container}>

                {qKey === "" && 
                <View style={styles.loginContainer}>
                <Text>Loading</Text>
                <ActivityIndicator animating={true} size="large" style={{opacity:1}} color="#999999" />
                </View>
                
                }  


                {qKey != "" &&     
                    <FlatList 
                data={playerNames}
                renderItem={({item, index}) => (
                    <View style={styles.container}>

                        <Table style={customStyles.tableTop} borderStyle={{borderWidth: 2, borderColor: '#c8e1ff'}}>
                            <Row data={titleHead} style={customStyles.head} textStyle={customStyles.text}/>
                            <Row data={(index==0) ? p1title : p2title} textStyle={customStyles.text}/>
                        </Table>

                        <TouchableOpacity
                            key = {index}
                            style={styles.button3}
                            onPress={() => dataPress(playerNames[index])}
                        >
                        
                            <Image
                                source={{ uri: playerUris[index] }}
                                
                                style={{flex:1, width: 210, height: 400, marginBottom: 10}}/>

                            <Text style={styles.homeScreenText}>
                                {item}</Text>
                            
                        </TouchableOpacity>
                        
                        
                        <Table borderStyle={{borderWidth: 2, borderColor: '#c8e1ff'}}>
                            <Row data={table1head} style={customStyles.head} textStyle={customStyles.text}/>
                            <Row data={(index==0) ? p1row1 : p2row1} textStyle={customStyles.text}/>
                        </Table>


                        <Table borderStyle={{borderWidth: 2, borderColor: '#c8e1ff'}}>
                            <Row data={table2head} style={customStyles.head} textStyle={customStyles.text}/>
                            <Row data={(index==0) ? p1row2 : p2row2} textStyle={customStyles.text}/>
                        </Table>
                        

                    </View>
            )}
            contentContainerStyle={{ flexGrow: 1 }}
            style={{ flex: 1 }}
            keyExtractor={(item, index) => index ? index.toString() : ""}
            numColumns={2} 
        />
                }
                
              
                

            
   

            

            
      </SafeAreaView>
    );
}

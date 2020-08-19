import React, { Component } from 'react';
import { StyleSheet, View, ScrollView, Text } from 'react-native';
import { Table, TableWrapper, Row } from 'react-native-table-component';

export default class App extends Component {


    constructor(props) {
        super(props);
        //let self = this;

        this.state = {
            "data": [],
            "tableState": "",
            "dataLoaded": false,
        };
        // let state = this.state;

        fetch(`http://10.0.2.2:5000?tickers=riot,gold,slv&investment=10000`, {
            method: "GET",
            // headers: headers,
        }).then((response) => response.text())
            .then((text) => {
                //console.log(text);
                console.log("ROWS")
                let rows = text.split("\n")
                let header = rows[0]
                header = header.split(",")
                console.log(header);
                let data = []

                // console.log("data array = ", data);
                for (let i=1; i<rows.length; i++) {
                    data.push(rows[i].split(","))
                }
                // console.log("Now data array = ");
                // console.log(data);
                let widthArray = [25]
                for (let i = 1; i<header.length; i++) {
                    widthArray.push(10+widthArray[i-1])
                }
                this.setState({
                    "data": data,
                    "tableState": {
                        "tableHead": header,
                        "widthArr": widthArray
                    },
                    "dataLoaded": true,
                });
                return text;
            })
            .catch((error) => {
                console.error(error);
            });
        // this.state = {
        //     tableHead: ['Head', 'Head2', 'Head3', 'Head4', 'Head5', 'Head6', 'Head7', 'Head8', 'Head9'],
        //     widthArr: [40, 60, 80, 100, 120, 140, 160, 180, 200]
        // }
    }

    // get_data() {
    //     return fetch(`http://localhost:5000?tickers=riot,gold,slv&investment=10000`, {
    //         method: "GET",
    //         // headers: headers,
    //     })
    // }

    render() {
        const state = this.state.tableState;
        let dataArray1 = this.state.data;
        const dataLoaded = this.state.dataLoaded
        dataArray1.pop()
        const dataArray = dataArray1.slice(0, 10);
        // const dataArray = [["50", "HAL", "2020-09-04", "17", "8.5", "0.0", "0.0", "0.9411764705882353", "0.0", "False"],
        //     ["51", "HAL", "2020-09-04", "17", "9.0", "0.0", "0.0", "0.8888888888888888", "0.0", "False"],
        //     ["52", "HAL", "2020-09-04", "17", "9.5", "0.0", "0.0", "0.8421052631578947", "0.0", "False"],
        //     ["53", "HAL", "2020-09-04", "17", "10.0", "0.0", "0.0", "0.8", "0.0", "False"]];



        console.log("In Render: Data Array =")
        console.log(dataArray[0])


       // console.log("THE DATA ARRAY DISCOVERED IN RENDER IS THE FOLLOWING: ")
       // console.log(dataArray)
        // for (let i = 0; i < 30; i += 1) {
        //     const dataRow = [];
        //     for (let j = 0; j < 9; j += 1) {
        //         dataRow.push(`${i}${j}`);
        //     }
        //     data.push(dataRow);
        // }

        console.log("Mapping")
        dataArray.map((dataRow, index) => console.log(dataRow))

        // return (
            if (dataLoaded) {
                return (<View style={styles.container}>
                    <ScrollView horizontal={true}>
                        <View>
                            {/*<Table borderStyle={{borderColor: '#C1C0B9'}}>*/}
                            {/*    <Row data={state.tableHead} widthArr={state.widthArr} style={styles.head} textStyle={styles.text}/>*/}
                            {/*</Table>*/}
                            <ScrollView style={styles.dataWrapper}>
                                <Table borderStyle={{borderColor: '#C1C0B9'}}>
                                    {
                                        dataArray.map((dataRow, index) => (
                                            <Row
                                                key={index}
                                                data={dataRow}
                                                widthArr={state.widthArr}
                                                style={[styles.row, index % 2 && {backgroundColor: '#ffffff'}]}
                                                textStyle={styles.text}
                                            />
                                        ))
                                    }
                                </Table>
                            </ScrollView>
                        </View>
                    </ScrollView>
                </View>)
            } else {
                return (<Text>Loading</Text>)
            }
       // )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        paddingTop: 30,
        backgroundColor: '#ffffff'
    },
    head: {
        height: 50,
        backgroundColor: '#6F7BD9'
    },
    text: {
        textAlign: 'center',
        fontWeight: '200'
    },
    dataWrapper: {
        marginTop: -1
    },
    row: {
        height: 40,
        backgroundColor: '#F7F8FA'
    }
});

import React, { useState, useEffect } from 'react'
import { Table, Tag, Space } from 'antd';
import { DatePicker } from 'antd';
import 'antd/dist/antd.css';

function App() {
    const [data, setData] = useState({})
    var milkContainer = document.getElementById("milk")

    useEffect(() => {
        fetch("/members").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                // console.log(data)
            }
        )
    }, [])

    const renderTable = () => {
        // console.log("data is ", Object.keys(data.cows[0]))
        const columns = Object.keys(data.cows[0]).map((mem, i) => {
            return {
                title: mem,
                dataIndex: mem,
                key: mem
            }
        })
        const tableData = data.cows

        console.log("columns ", columns)
        console.log("tableData ", tableData)


        return <Table columns={columns} dataSource={tableData} />


    }

    return (
        <div>
            {(typeof data.cows === 'undefined') ? (
                <p> Loading ... </p>
            ) :
                renderTable()
            }


        </div>
    )
}

export default App
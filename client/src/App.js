import React, { useState, useEffect } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';



function App() {
    const [data, setData] = useState({})

    useEffect(() => {
        fetch("/weather").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])

    function onChange(pagination, filters, sorter, extra) {
        console.log('params', pagination, filters, sorter, extra);
    }

    const renderTable = () => {
        console.log("data is ", Object.keys(data.weather[0]))
        const columns = Object.keys(data.weather[0]).map((mem, i) => {
            console.log("-------", mem, i)
            return {
                title: mem,
                dataIndex: mem,
                key: mem,
                sorter: (a, b) => a[mem] - b[mem],
                defaultSortOrder: mem === 'Date' ? 'descend' : console.log()
            }
        })
        const tableData = data.weather

        console.log("columns ", columns)
        // console.log("tableData ", tableData)


        return <Table columns={columns} dataSource={tableData} onChange={onChange} />


    }

    return (
        <div>
            {(typeof data.weather === 'undefined') ? (
                <p> Loading ... </p>
            ) :
                renderTable()
            }


        </div>
    )
}

export default App
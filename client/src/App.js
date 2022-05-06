import React, { useState, useEffect } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';
import { DualAxes } from '@ant-design/plots';
import { yellow } from '@mui/material/colors';


function App() {
    const [data, setData] = useState({})
    console.log("-----here1")
    useEffect(() => {
        fetch("/sum").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log("-----here2")
                console.log(data)
            }
        )
    }, [])

    function onChange(pagination, filters, sorter, extra) {
        console.log('params', pagination, filters, sorter, extra);
    }

    const renderTableMilk = () => {
        console.log("data is ", Object.keys(data.milk[0]))
        const columns = Object.keys(data.milk[0]).map((mem, i) => {
            console.log("-------", mem, i)
            return {
                title: mem,
                dataIndex: mem,
                key: mem,
                sorter: function (a, b) {
                    if (mem === 'Date') {
                        return new Date(a[mem]) - new Date(b[mem])
                    } else if (mem === 'Lactation number') {
                        if (a[mem] === '3+') {
                            return 1
                        }
                        if (b[mem] === '3+') {
                            return -1
                        }
                        return a[mem] - b[mem]
                    }
                    return a[mem] - b[mem]
                },
                defaultSortOrder: mem === 'Date' ? 'descend' : console.log()
            }
        })
        const tableData = data.milk

        console.log("columns ", columns)
        // console.log("tableData ", tableData)


        return <Table columns={columns} dataSource={tableData} onChange={onChange} />
    }

    const renderTableWeather = () => {
        console.log("data is ", Object.keys(data.weather[0]))
        const columns = Object.keys(data.weather[0]).map((mem, i) => {
            console.log("-------", mem, i)
            return {
                title: mem,
                dataIndex: mem,
                key: mem,
                sorter: function (a, b) {
                    if (mem === 'Date') {
                        return new Date(a[mem]) - new Date(b[mem])
                    } else if (mem === 'Lactation number') {
                        if (a[mem] === '3+') {
                            return 1
                        }
                        if (b[mem] === '3+') {
                            return -1
                        }
                        return a[mem] - b[mem]
                    }
                    return a[mem] - b[mem]
                },
                defaultSortOrder: mem === 'Date' ? 'descend' : console.log()
            }
        })
        const tableData = data.weather

        console.log("columns ", columns)
        // console.log("tableData ", tableData)


        return <Table columns={columns} dataSource={tableData} onChange={onChange} />
    }

    const DemoDualAxes = () => {
        const dataChart = data.sum
        const config = {
            data: [dataChart, dataChart],
            xField: 'Date',
            yField: ['Average yield (lb)', 'Average temperature (°C)'],
            geometryOptions: [
                {
                    geometry: 'line',
                    smooth: true,
                    color: '#5B8FF9',
                    lineStyle: {
                        lineWidth: 3,
                    },
                },
                {
                    geometry: 'line',
                    smooth: true,
                    color: '#5AD8A6',
                    lineStyle: {
                        lineWidth: 3,
                    },
                },
            ],
        };
        return <DualAxes {...config} />;
    };

    return (
        <div>
            <div class="row">
                <div class="col-xl-12 col-lg-12">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                            <h6 class="m-0 font-weight-bold text-primary">Milk Daily Overview</h6>
                        </div>
                        <div class="card-body">
                            <div>
                                {(typeof data.milk === 'undefined') ? (
                                    <p> Loading ... </p>
                                ) : renderTableMilk()
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-xl-12 col-lg-12">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                            <h6 class="m-0 font-weight-bold text-primary">Weather Overview</h6>
                        </div>
                        <div class="card-body">
                            <div>
                                {(typeof data.weather === 'undefined') ? (
                                    <p> Loading ... </p>
                                ) : renderTableWeather()
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-xl-12 col-lg-12">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                            <h6 class="m-0 font-weight-bold text-primary">Milk Daily vs Weather Chart</h6>
                        </div>
                        <div class="card-body">
                            <div>
                                {(typeof data.sum === 'undefined') ? (
                                    <p> Loading ... </p>
                                ) :
                                    <DemoDualAxes />
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>



    )
}

export default App
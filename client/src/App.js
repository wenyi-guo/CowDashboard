import React, { useState, useEffect } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';
import { DualAxes } from '@ant-design/plots';


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

    const DemoDualAxes = () => {
        const dataChart = data.sum
        const cow = [
            {
                "Yield(gr)": 1160714,
                "Date": 1521432000
            },
            {

                "Yield(gr)": 257949,
                "Date": 1521432022
            },
            {
                "Yield(gr)": 85665,
                "Date": 1521432003
            },
        ]
        const testdata = [
            {
                year: '1991',
                value: 3,
                count: 10,
            },
            {
                year: '1992',
                value: 4,
                count: 4,
            },
            {
                year: '1994',
                value: 5,
                count: 5,
            },
        ];
        const config = {
            data: [dataChart, dataChart],
            xField: 'Date',
            yField: ['avg_Yield(gr)', 'avg_temp'],
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
                                {(typeof data.weather === 'undefined') ? (
                                    <p> Loading ... </p>
                                ) : renderTable()
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
                                {(typeof data.weather === 'undefined') ? (
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
import React, { useState, useEffect } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';
import { DualAxes } from '@ant-design/plots';

function onChange(pagination, filters, sorter, extra) {
    // console.log('params', pagination, filters, sorter, extra);
}
const renderTableMilk = (data) => {
    // console.log("data is ", Object.keys(data.milk[0]))
    const columns = Object.keys(data.milk[0]).map((mem, i) => {
        // console.log("-------", mem, i)
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



    return <Table columns={columns} dataSource={tableData} onChange={onChange} />
}

const renderTableWeather = (data) => {
    // console.log("data is ", Object.keys(data.weather[0]))
    const columns = Object.keys(data.weather[0]).map((mem, i) => {
        // console.log("-------", mem, i)
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

    // console.log("columns ", columns)
    // console.log("tableData ", tableData)


    return <Table columns={columns} dataSource={tableData} onChange={onChange} />
}

const renderDemoDualAxes = (data) => {
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


const Milk = (props) => {
    return <div>
        <div className="row">
            <div className="col-xl-12 col-lg-12">
                <div className="card shadow mb-4">
                    <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                        <h6 className="m-0 font-weight-bold text-primary">Milk Daily Overview</h6>
                    </div>
                    <div className="card-body">
                        <div>
                            {(typeof props.data.milk === 'undefined') ? (
                                <p> Loading ... </p>
                            ) : renderTableMilk(props.data)
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div className="row">
            <div className="col-xl-12 col-lg-12">
                <div className="card shadow mb-4">
                    <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                        <h6 className="m-0 font-weight-bold text-primary">Weather Overview</h6>
                    </div>
                    <div className="card-body">
                        <div>
                            {(typeof props.data.weather === 'undefined') ? (
                                <p> Loading ... </p>
                            ) : renderTableWeather(props.data)
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div className="row">
            <div className="col-xl-12 col-lg-12">
                <div className="card shadow mb-4">
                    <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                        <h6 className="m-0 font-weight-bold text-primary">Milk Daily vs Weather Chart</h6>
                    </div>
                    <div className="card-body">
                        <div>
                            {(typeof props.data.sum === 'undefined') ? (
                                <p> Loading ... </p>
                            ) : renderDemoDualAxes(props.data)
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

}

export default Milk
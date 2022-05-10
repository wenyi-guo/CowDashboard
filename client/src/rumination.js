import React, { useState, useEffect } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';
import { DualAxes } from '@ant-design/plots';

function onChange(pagination, filters, sorter, extra) {
    // console.log('params', pagination, filters, sorter, extra);
}
const renderTableRum = (data) => {
    const columns = Object.keys(data.rum[0]).map((mem, i) => {
        return {
            title: mem,
            dataIndex: mem,
            key: mem,
            sorter: function (a, b) {
                if (mem === 'Date') {
                    return new Date(a[mem]) - new Date(b[mem])
                }
                return a[mem] - b[mem]
            },
            defaultSortOrder: mem === 'Date' ? 'descend' : console.log()
        }
    })
    const tableData = data.rum



    return <Table columns={columns} dataSource={tableData} onChange={onChange} />
}

const renderTableWeather = (data) => {
    const columns = Object.keys(data.weather[0]).map((mem, i) => {
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

    return <Table columns={columns} dataSource={tableData} onChange={onChange} />
}

const renderDemoDualAxes = (data) => {
    const weatherChart = data.weather
    const rumChart = data.rum
    const config = {
        data: [rumChart, weatherChart],
        xField: 'Date',
        yField: ['Average rumination', 'Average temperature (°C)'],
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

const renderDemoDualAxes2 = (data) => {
    const weatherChart = data.weather
    const rumChart = data.rum
    const config = {
        data: [rumChart, weatherChart],
        xField: 'Date',
        yField: ['Average eating', 'Average temperature (°C)'],
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


const Rum = (props) => {
    return <div>
        <div className="row">
            <div className="col-xl-12 col-lg-12">
                <div className="card shadow mb-4">
                    <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                        <h6 className="m-0 font-weight-bold text-primary">Rumination Overview</h6>
                    </div>
                    <div className="card-body">
                        <div>
                            {(typeof props.data.milk === 'undefined') ? (
                                <p> Loading ... </p>
                            ) : renderTableRum(props.data)
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
                        <h6 className="m-0 font-weight-bold text-primary">Rumination vs Weather Chart</h6>
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

        <div className="row">
            <div className="col-xl-12 col-lg-12">
                <div className="card shadow mb-4">
                    <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                        <h6 className="m-0 font-weight-bold text-primary">Eating vs Weather Chart</h6>
                    </div>
                    <div className="card-body">
                        <div>
                            {(typeof props.data.sum === 'undefined') ? (
                                <p> Loading ... </p>
                            ) : renderDemoDualAxes2(props.data)
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

}

export default Rum
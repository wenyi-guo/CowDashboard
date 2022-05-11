import React, { useState, useEffect, useCallback } from 'react'
import { Table } from 'antd';
// import 'antd/dist/antd.less';
import 'antd/dist/antd.css';
import { DualAxes } from '@ant-design/plots';
import Milk from './milk';
import Rum from './rumination';


function App() {
    const [data, setData] = useState({})
    const [type, setType] = useState("milk-type")
    const fetchData = useCallback(async () => {
        console.log("----------REFRESH---");
        try {
            fetch("/sum").then(
                res => res.json()
            ).then(
                data => {
                    setData(data)
                }
            )
        }
        catch (err) {
            console.log(err);
        }
    }, []);
    useEffect(() => {
        fetchData();
        const interval = setInterval(() => {
            fetchData();
        }, 2000);
        return () => clearInterval(interval);
    }, [fetchData]);

    // useEffect(() => {
    //     fetch("/sum").then(
    //         res => res.json()
    //     ).then(
    //         data => {
    //             setData(data)
    //         }
    //     )
    // }, [])




    const renderTab = () => {
        let ret = type == "milk-type" ? <Milk data={data} /> : <Rum data={data} />

        const handleType = (event) => {
            setType(event.target.id)
        }



        return <div>
            <div id="wrapper">

                {/* <!-- Sidebar --> */}
                <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">


                    <a className="sidebar-brand d-flex align-items-center justify-content-center">

                    </a>

                    {/* <!-- Divider --> */}
                    <div className="sidebar-divider my-0"></div>

                    {/* <!-- Nav Item - Dashboard --> */}
                    <li className="nav-item active">
                        <a className="nav-link">
                            <i className="fas fa-fw fa-tachometer-alt"></i>
                            <span id="milk-type" onClick={handleType}>Milk Daily</span></a>
                    </li>

                    <div className="sidebar-divider my-0"></div>


                    <div className="sidebar-divider my-0"></div>


                    <li className="nav-item active">
                        <a className="nav-link">
                            <i className="fas fa-fw fa-tachometer-alt"></i>
                            <span id="rumination-type" onClick={handleType}>Rumination</span></a>
                    </li>

                </ul>

                <div id="content-wrapper" className="d-flex flex-column">

                    {/* <!-- Main Content --> */}
                    <div id="content">

                        {/* <!-- Topbar --> */}
                        <nav className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
                            {/* <!-- Page Heading --> */}
                            <div className="d-sm-flex align-items-center justify-content-between mb-4">
                                <h1 className="h3 mb-0 text-gray-800" id="title" >Cow Performance Dashboard</h1>
                            </div>

                            {/* <!-- Sidebar Toggle (Topbar) --> */}
                            <button id="sidebarToggleTop" className="btn btn-link d-md-none rounded-circle mr-3">
                                <i className="fa fa-bars"></i>
                            </button>




                        </nav>
                        {/* <!-- End of Topbar --> */}

                        {/* <!-- Begin Page Content --> */}
                        <div className="container-fluid">



                            <div id="milk">
                                {ret}

                            </div>

                        </div>
                    </div>

                </div>

            </div>

        </div>
    }


    return (
        <div>
            {renderTab()}
            {/* <Milk data={data} /> */}
        </div>

    )
}

export default App
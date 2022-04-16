import React, {useState, useEffect} from 'react'

function App() {
    const [data, setData] = useState({})

    useEffect(() => {
      fetch("/members").then(
          res => res.json()
      ).then(
          data => {
            setData(data)
            console.log(data)
          }
      )
    }, [])

    return (
        <div>
            {(typeof data.cows === 'undefined')? (
                <p> Loading ... </p>
            ) : (
                data.cows.map((member, i) => (
                    <p key={i}>{JSON.stringify(member)}</p>
                )) 
            )}

            
        </div>
    )
}

export default App
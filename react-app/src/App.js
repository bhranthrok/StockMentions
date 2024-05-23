import {useState, useEffect, useCallback} from 'react'

function App() {
  const [data, setData] = useState({stocks: [], mentions: []})
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState(null)

  const [postLimit, setPostLimit] = useState(10)
  const [sortingMethod, setSortingMethod] = useState("hot")
  const [minMentions, setMinMentions] = useState(2)

  const totalPosts = postLimit*9

  const refreshData = useCallback(() => {
    setLoading(true)
    setLoaded(false)
    setError(null)

    fetch(`http://localhost:5000/mentions?postLimit=${postLimit}&sortingMethod=${sortingMethod}&minMentions=${minMentions}`)
      .then(
        res => {
          if (!res.ok) {
            throw new Error("Response not ok")
          }
          return res.json()
        }
      )
      .then(data => {
        setData(data);
        setLoading(false)
        setLoaded(true)
        console.log(data)
      })
      .catch(error => {
        setError(error.message);
        setLoading(false)
      })
  }, [postLimit, sortingMethod, minMentions])

  const handlePostLimitChange = (event) => {
    setPostLimit(Number(event.target.value))
  }
  const handleSortingMethodChange = (event) => {
    setSortingMethod(event.target.value)
  }
  const handleMinMentionsChange = (event) => {
    setMinMentions(Number(event.target.value))
  }

  let content;

  if (loading) { 
      content = (<div>
      <br />
      Loading... Please wait a few seconds.
      </div>
      )
  }

  else if (error) {
      content = ( <div>
      <br />
      Error: {error}, try again later
      </div>
      )
  }

  else if (loaded) {
    content = (
      <table>
        <thead>
          <tr>
            <th>Stock</th>
            <th>Mentions</th>
          </tr>
        </thead>
        <tbody>
          {data.stocks.map((stock, index) => (
            <tr key={index}>
              <td className='stockColumn'>{stock}</td>
              <td className='mentionsColumn'>{data.mentions[index]}</td>
            </tr>
          ))}
        </tbody>
      </table>

    )
  }

  return (
    <div>
      <h1 className='title'>$tockMentions</h1>

      <div className='filters'>
        <label className='postNumber'>
          Number of Posts (per subreddit):
          <input 
          type = "number"
          value = {postLimit}
          onChange={handlePostLimitChange}
          min = "1"
          />
        </label>
        
        <label className='sort'>
          Sort:
          <select value={sortingMethod} onChange={handleSortingMethodChange}>
            <option value = "hot">Hot</option>
            <option value = "new">New</option>
            <option value = "top">Top</option>
            <option value = "rising">Rising</option>
          </select>
        </label>

        <label className='min'>
          Minimum:
          <input 
          type = "number"
          value = {minMentions}
          onChange={handleMinMentionsChange}
          min = "1"
          />
        </label>
      </div>
      
      <br />

      <p className='totalPosts'>Total Posts: {totalPosts}</p>

      <button onClick={refreshData}>Refresh</button>

      {content}

      <br />

      
    </div>
  );
}

export default App;

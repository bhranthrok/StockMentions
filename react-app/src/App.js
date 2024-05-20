import {useState, useEffect, useCallback} from 'react'

function App() {
  const [data, setData] = useState({stocks: [], mentions: []})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [postLimit, setPostLimit] = useState(2)
  const [sortingMethod, setSortingMethod] = useState("hot")
  const [minMentions, setMinMentions] = useState(1)

  const refreshData = useCallback(() => {
    setLoading(true)
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

  if (loading) {
    return <div>
      <h1>StockMentions</h1>
      <p>Click refresh below to analyze hundreds of posts across several stock trading subreddits.</p>
      <button>Refresh</button>
      <br />
      Loading... Please wait a few seconds.
      </div>
  }

  if (error) {
    return <div>
      <h1>StockMentions</h1>
      <p>Click refresh below to analyze hundreds of posts across several stock trading subreddits.</p>
      <button onClick={refreshData}>Refresh</button>
      <br />
      Error: {error}, try again later</div>
  }

  return (
    <div>
      <h1>StockMentions</h1>
      
      <p>Click refresh below to analyze hundreds of posts across several stock trading subreddits.</p>
      
      <label>
        Number of Posts(per subreddit):
        <input 
        type = "number"
        value = {postLimit}
        onChange={handlePostLimitChange}
        min = "1"
        />
      </label>
      
      <label>
        Sort:
        <select value={sortingMethod} onChange={handleSortingMethodChange}>
          <option value = "hot">Hot</option>
          <option value = "new">New</option>
          <option value = "top">Top</option>
          <option value = "rising">Rising</option>
        </select>
      </label>

      <label>
        Minimum:
        <input 
        type = "number"
        value = {minMentions}
        onChange={handleMinMentionsChange}
        min = "1"
        />
      </label>
      
      <br />
      
      <button onClick={refreshData}>Refresh</button>

      <br />

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
              <td>{stock}</td>
              <td>{data.mentions[index]}</td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}

export default App;

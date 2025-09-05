// import React, { useEffect, useState } from "react";
// import NewsItems from "./NewsItems";
// import Spinner from "./Spinner";
// import PropTypes from "prop-types";
// import InfiniteScroll from "react-infinite-scroll-component";

// const News = (props) => {
//   const [articles, setArticles] = useState([]); // State to store articles
//   const [loading, setLoading] = useState(true); // State to handle loading spinner
//   const [page, setPage] = useState(1); // State for current page
//   const [totalResults, setTotalResults] = useState(0); // Total results from the API

//   // Capitalize the first letter of a string
//   const capitalizeFirstLetter = (string) => {
//     return string.charAt(0).toUpperCase() + string.slice(1);
//   };

//   // Fetch news articles and update the state
//   const updateNews = async () => {
//     props.setProgress(10);
//     const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${page}&pageSize=${props.pageSize}`;
//     setLoading(true);
//     try {
//       let data = await fetch(url);
//       props.setProgress(30);
//       let parsedData = await data.json();
//       props.setProgress(70);
//       setArticles(parsedData.articles || []);
//       setTotalResults(parsedData.totalResults || 0);
//       setLoading(false);
//       props.setProgress(100);
//     } catch (error) {
//       console.error("Failed to fetch news:", error);
//       setLoading(false);
//     }
//   };

//   const fetchMoreData = async () => {
//     const url = `https://newsapi.org/v2/top-headlines?country=${
//       props.country
//     }&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${
//       page + 1
//     }&pageSize=${props.pageSize}`;
//     setPage((prevPage) => prevPage + 1);
//     try {
//       let data = await fetch(url);
//       let parsedData = await data.json();
//       setArticles((prevArticles) =>
//         prevArticles.concat(parsedData.articles || [])
//       );
//       setTotalResults(parsedData.totalResults || 0);
//     } catch (error) {
//       console.error("Failed to fetch more news:", error);
//     }
//   };

//   // Effect to fetch news on component mount
//   useEffect(() => {
//     document.title = `${capitalizeFirstLetter(props.category)} - NewsUpdate`;
//     updateNews();
//     // eslint-disable-next-line
//   }, []); // Empty dependency array ensures this runs only once

//   return (
//     <>
//       <h1
//         className="text-center"
//         style={{ margin: "35px 0px", marginTop: "90px" }}
//       >
//         NewsUpdate - Top {capitalizeFirstLetter(props.category)} Headlines
//       </h1>
//       {loading && <Spinner />} {/* Show spinner while loading */}
//       <InfiniteScroll
//         dataLength={articles ? articles.length : 0} // Handle undefined safely
//         next={fetchMoreData}
//         hasMore={articles.length < totalResults} // Check if there are more articles to load
//         loader={<Spinner />} // Spinner for infinite scroll loading
//       >
//         <div className="container">
//           <div className="row">
//             {articles.map((element) => (
//               <div className="col-md-4" key={element.url}>
//                 <NewsItems
//                   title={element.title || "No Title Available"}
//                   description={
//                     element.description || "No Description Available"
//                   }
//                   imageUrl={element.urlToImage}
//                   newsUrl={element.url}
//                   author={element.author}
//                   date={element.publishedAt}
//                   source={element.source.name}
//                 />
//               </div>
//             ))}
//           </div>
//         </div>
//       </InfiniteScroll>
//     </>
//   );
// };

// // Default props for the News component
// News.defaultProps = {
//   country: "us",
//   pageSize: 8,
//   category: "general",
// };

// // Prop types for the News component
// News.propTypes = {
//   country: PropTypes.string,
//   pageSize: PropTypes.number,
//   category: PropTypes.string,
//   setProgress: PropTypes.func.isRequired,
// };

// export default News;

import React, { useEffect, useState } from "react";
import NewsItems from "./NewsItems";
import Spinner from "./Spinner";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";

const News = (props) => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);

  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const updateNews = async () => {
    props.setProgress(10);
    const url = `http://localhost:3001/api/news?country=${props.country}&category=${props.category}&page=${page}&pageSize=${props.pageSize}`;
    setLoading(true);
    try {
      let data = await fetch(url);
      props.setProgress(30);
      let parsedData = await data.json();
      props.setProgress(70);
      setArticles(parsedData.articles || []);
      setTotalResults(parsedData.totalResults || 0);
      setLoading(false);
      props.setProgress(100);
    } catch (error) {
      console.error("Failed to fetch news:", error);
      setLoading(false);
    }
  };

  const fetchMoreData = async () => {
    const nextPage = page + 1;
    const url = `http://localhost:3001/api/news?country=${props.country}&category=${props.category}&page=${nextPage}&pageSize=${props.pageSize}`;
    setPage(nextPage);
    try {
      let data = await fetch(url);
      let parsedData = await data.json();
      setArticles((prevArticles) =>
        prevArticles.concat(parsedData.articles || [])
      );
      setTotalResults(parsedData.totalResults || 0);
    } catch (error) {
      console.error("Failed to fetch more news:", error);
    }
  };

  useEffect(() => {
    document.title = `${capitalizeFirstLetter(props.category)} - NewsUpdate`;
    updateNews();
    // eslint-disable-next-line
  }, []);

  return (
    <>
      <h1
        className="text-center"
        style={{ margin: "35px 0px", marginTop: "90px" }}
      >
        NewsUpdate - Top {capitalizeFirstLetter(props.category)} Headlines
      </h1>
      {loading && <Spinner />}
      <InfiniteScroll
        dataLength={articles ? articles.length : 0}
        next={fetchMoreData}
        hasMore={articles.length < totalResults}
        loader={<Spinner />}
      >
        <div className="container">
          <div className="row">
            {articles.map((element) => (
              <div className="col-md-4" key={element.url}>
                <NewsItems
                  title={element.title || "No Title Available"}
                  description={
                    element.description || "No Description Available"
                  }
                  imageUrl={element.urlToImage}
                  newsUrl={element.url}
                  author={element.author}
                  date={element.publishedAt}
                  source={element.source.name}
                />
              </div>
            ))}
          </div>
        </div>
      </InfiniteScroll>
    </>
  );
};

News.defaultProps = {
  country: "us",
  pageSize: 8,
  category: "general",
};

News.propTypes = {
  country: PropTypes.string,
  pageSize: PropTypes.number,
  category: PropTypes.string,
  setProgress: PropTypes.func.isRequired,
};

export default News;

import React, { useEffect, useState } from "react";
import NewsItems from "./NewsItems";
import Spinner from "./Spinner";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";

const News = (props) => {
  const [articles, setArticles] = useState([]); // State to store articles
  const [loading, setLoading] = useState(true); // State to handle loading spinner
  const [page, setPage] = useState(1); // State for current page
  const [totalResults, setTotalResults] = useState(0); // Total results from the API

  // Capitalize the first letter of a string
  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  // Fetch news articles and update the state
  const updateNews = async () => {
    props.setProgress(10); // Update progress bar
    const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${page}&pageSize=${props.pageSize}`;
    setLoading(true); // Show spinner while loading
    try {
      let data = await fetch(url);
      props.setProgress(30);
      let parsedData = await data.json();
      props.setProgress(70);
      setArticles(parsedData.articles || []); // Safely update articles
      setTotalResults(parsedData.totalResults || 0); // Safely update total results
      setLoading(false); // Hide spinner after loading
      props.setProgress(100); // Complete progress bar
    } catch (error) {
      console.error("Failed to fetch news:", error);
      setLoading(false); // Ensure loading spinner is hidden on error
    }
  };

  // Fetch more articles for infinite scrolling
  const fetchMoreData = async () => {
    const url = `https://newsapi.org/v2/top-headlines?country=${
      props.country
    }&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${
      page + 1
    }&pageSize=${props.pageSize}`;
    setPage((prevPage) => prevPage + 1);
    try {
      let data = await fetch(url);
      let parsedData = await data.json();
      setArticles((prevArticles) =>
        prevArticles.concat(parsedData.articles || [])
      ); // Concatenate new articles
      setTotalResults(parsedData.totalResults || 0); // Update total results if available
    } catch (error) {
      console.error("Failed to fetch more news:", error);
    }
  };

  // Effect to fetch news on component mount
  useEffect(() => {
    document.title = `${capitalizeFirstLetter(props.category)} - NewsUpdate`;
    updateNews();
    // eslint-disable-next-line
  }, []); // Empty dependency array ensures this runs only once

  return (
    <>
      <h1
        className="text-center"
        style={{ margin: "35px 0px", marginTop: "90px" }}
      >
        NewsUpdate - Top {capitalizeFirstLetter(props.category)} Headlines
      </h1>
      {loading && <Spinner />} {/* Show spinner while loading */}
      <InfiniteScroll
        dataLength={articles ? articles.length : 0} // Handle undefined safely
        next={fetchMoreData}
        hasMore={articles.length < totalResults} // Check if there are more articles to load
        loader={<Spinner />} // Spinner for infinite scroll loading
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

// Default props for the News component
News.defaultProps = {
  country: "us",
  pageSize: 8,
  category: "general",
};

// Prop types for the News component
News.propTypes = {
  country: PropTypes.string,
  pageSize: PropTypes.number,
  category: PropTypes.string,
  setProgress: PropTypes.func.isRequired,
};

export default News;

//Class Based Component

// import React, { Component } from "react";
// import NewsItems from "./NewsItems";
// import Spinner from "./Spinner";
// import PropTypes from "prop-types";
// import InfiniteScroll from "react-infinite-scroll-component";

// export class News extends Component {
//   static defaultProps = {
//     country: "us",
//     pageSize: 8,
//     category: "general",
//   };

//   static propTypes = {
//     country: PropTypes.string,
//     pageSize: PropTypes.number,
//     category: PropTypes.string,
//   };
//   capitalizeFirstLetter = (string) => {
//     return string.charAt(0).toUpperCase() + string.slice(1);
//   };

//   constructor(props) {
//     super(props);
//     console.log("Hello I am a Constructor from NewsComponent");
//     this.state = {
//       articles: [],
//       loading: true,
//       page: 1,
//       totalResults: 0,
//     };
//     document.title = `${this.capitalizeFirstLetter(
//       props.category
//     )} - NewsUpdate`;
//   }

//   async updateNews() {
//     props.setProgress(10);
//     const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${this.state.page}&pageSize=
//     ${props.pageSize}`;
//     this.setState({ loading: true });
//     let data = await fetch(url);
//     props.setProgress(30);
//     let parsedData = await data.json();
//     props.setProgress(70);
//     console.log(parsedData);
//     this.setState({
//       articles: parsedData.articles,
//       totalResults: parsedData.totalResults,
//       loading: false,
//     });
//     props.setProgress(100);
//   }

//   async componentDidMount() {
//     this.updateNews();
//   }

//   handlePrevClick = async () => {
//     this.setState({ page: this.state.page - 1 });
//     this.updateNews();
//   };

//   handleNextClick = async () => {
//     console.log("Next");
//     this.setState({ page: this.state.page + 1 });
//     this.updateNews();
//   };
//   fetchMoreData = async () => {
//     this.setState({ page: this.state.page + 1 });
//     const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=11e2c80f95584684a9a6f1849b8c4c48&page=${this.state.page}&pageSize=
//     ${props.pageSize}`;
//     // this.setState({ loading: true });
//     let data = await fetch(url);
//     let parsedData = await data.json();
//     console.log(parsedData);
//     this.setState({
//       articles: this.state.articles.concat(parsedData.articles),
//       totalResults: parsedData.totalResults,
//       // loading: false,
//     });
//   };

//   render() {
//     return (
//       <>
//         <h1 className="text-center" style={{ margin: "35px 0px" }}>
//           NewsUpdate - Top
//           {""} {this.capitalizeFirstLetter(props.category)} Headlines
//         </h1>
//         {this.state.loading && <Spinner />}
//         <InfiniteScroll
//           dataLength={this.state.articles.length}
//           next={this.fetchMoreData}
//           hasMore={this.state.articles.length !== this.state.totalResults}
//           loader={<Spinner />}
//         >
//           <div className="container">
//             <div className="row">
//               {/* {!this.state.loading && */}
//               {this.state.articles.map((element) => {
//                 return (
//                   <div className="col-md-4" key={element.url}>
//                     <NewsItems
//                       title={element.title ? element.title : ""}
//                       description={
//                         element.description ? element.description : ""
//                       }
//                       imageUrl={element.urlToImage}
//                       newsUrl={element.url}
//                       author={element.author}
//                       date={element.publishedAt}
//                       source={element.source.name}
//                     />
//                   </div>
//                 );
//               })}
//             </div>
//           </div>
//         </InfiniteScroll>
//         {/* <div className="container d-flex justify-content-between">
//           <button
//             disabled={this.state.page <= 1}
//             type="button"
//             className="btn btn-dark"
//             onClick={this.handlePrevClick}
//           >
//             &larr;Previous
//           </button>
//           <button
//             disabled={
//               this.state.page + 1 >
//               Math.ceil(this.state.totalResults / props.pageSize)
//             }
//             type="button"
//             className="btn btn-dark"
//             onClick={this.handleNextClick}
//           >
//             Next&rarr;
//           </button>
//         </div> */}
//       </>
//     );
//   }
// }

// export default News;

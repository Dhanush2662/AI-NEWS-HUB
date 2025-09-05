export default async function handler(req, res) {
  const {
    country = "us",
    category = "general",
    page = 1,
    pageSize = 8,
  } = req.query;

  const apiKey = "11e2c80f95584684a9a6f1849b8c4c48"; // Your NewsAPI key

  const url = `https://newsapi.org/v2/top-headlines?country=${country}&category=${category}&apiKey=${apiKey}&page=${page}&pageSize=${pageSize}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to fetch news" });
  }
}

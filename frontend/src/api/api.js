import axios from "axios";

const BASE_URL = "https://sentiment-analyzer-asdz.onrender.com";

export const getReviews = async (productName) => {
  const response = await axios.get(`${BASE_URL}/api/reviews`, {
    params: { product: productName },
  });
  return response.data;
};

export const getSentiment = async (productName) => {
  const response = await axios.get(`${BASE_URL}/api/sentiment`, {
    params: { product: productName },
  });
  return response.data;
};

export const getProducts = async () => {
  const response = await axios.get(`${BASE_URL}/api/products`);
  return response.data;
};

export const scrapeProduct = async (productName) => {
  const response = await axios.post(`${BASE_URL}/api/scrape`, {
    product_name: productName,
  });
  return response.data;
};

export const checkScrapeStatus = async (productName) => {
  const response = await axios.get(`${BASE_URL}/api/scrape/status`, {
    params: { product: productName },
  });
  return response.data;
};
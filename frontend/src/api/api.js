import axios from "axios";

// Base URL of our Flask backend
// All API calls will start with this
const BASE_URL = "http://127.0.0.1:5000";

// Fetch all reviews for a product
export const getReviews = async (productName) => {
  const response = await axios.get(`${BASE_URL}/api/reviews`, {
    params: { product: productName },
  });
  return response.data;
};

// Fetch sentiment summary for a product
export const getSentiment = async (productName) => {
  const response = await axios.get(`${BASE_URL}/api/sentiment`, {
    params: { product: productName },
  });
  return response.data;
};

// Fetch all products stored in database
export const getProducts = async () => {
  const response = await axios.get(`${BASE_URL}/api/products`);
  return response.data;
};

// Trigger scraping for a new product
export const scrapeProduct = async (productName) => {
  const response = await axios.post(`${BASE_URL}/api/scrape`, {
    product_name: productName,
  });
  return response.data;
};
const API_SERVER = "http://localhost:8000";

const signup = async (username, password) => {
  const response = await fetch(`${API_SERVER}/signup/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  return await response.json();
};

const login = async (username, password) => {
  const response = await fetch(`${API_SERVER}/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include", // Important for session cookies
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  return await response.json();
};

const logout = async () => {
  const response = await fetch(`${API_SERVER}/logout/`, {
    method: "POST",
    credentials: "include",
  });
  return await response.json();
};

const viewPost = async (postId) => {
  const response = await fetch(`${API_SERVER}/view/${postId}/`);
  return await response.json();
};

const getTimeline = async (count) => {
  const response = await fetch(`${API_SERVER}/timeline/${count}/`);
  return await response.json();
};

const likePost = async (postId) => {
  const response = await fetch(`${API_SERVER}/like/${postId}/`);
  return await response.json();
};

const createPost = async (content, relatedPostId = null) => {
  const response = await fetch(`${API_SERVER}/post/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
      content: content,
      related: relatedPostId,
    }),
  });
  return await response.json();
};

const editPost = async (postId, content, relatedPostId = null) => {
  const response = await fetch(`${API_SERVER}/edit/${postId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
      content: content,
      related: relatedPostId,
    }),
  });
  return await response.json();
};

const deletePost = async (postId) => {
  const response = await fetch(`${API_SERVER}/delete/${postId}/`, {
    method: "POST",
    credentials: "include",
  });
  return await response.json();
};

const formatDate = (date) => {
  date = new Date(date * 1000);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")} ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
};

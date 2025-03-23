# 🧠 Deepskin Frontend

A web interface for Deepskin — an AI-powered tool that classifies skin marks using a machine learning model.  
Users input demographic info and upload an image of a skin lesion. The system analyzes the image and predicts the type of skin condition.

---

## 🚀 Features

- Multi-step or single-page form to collect:
  - Sex
  - Age
  - Body localization
  - Skin mark image
- Real-time AI prediction via Flask API
- Displays result in an embedded HTML report
- Info panel on common skin conditions

---

## 🧪 Local Development

### 🔁 Backend Setup

1. **Google Cloud Credentials**  
   - Go to **Google Console** → **IAM & Admin** → **Service Accounts**  
   - Generate a new key  
   - Rename the key file to `credentials.json`  
   - Place it in the root of your `Deepskin` directory

2. **Run the API with Docker**

From the `Deepskin` directory:

```bash
docker build -f deployment/Dockerfile -t deepskin_api .
docker run -p 5100:5100 --name deepskin_container deepskin_api
```

Backend should be available at:  
👉 http://127.0.0.1:5100

---

### 🎨 Frontend Setup

From the `Deepskin/front` directory:

1. **Install Node.js and npm** (if not already installed)

2. **Install dependencies:**

```bash
npm install
```

3. **Install Axios (for API requests):**

```bash
npm install axios
```

4. **Set up proxy to backend:**

In `package.json`, add:

```json
"proxy": "http://127.0.0.1:5100",
```

5. **Start the React app:**

```bash
npm start
```

Frontend will be live at:  
👉 http://localhost:3000

---

## 🛠 Notes

- Ensure the backend is running **before** submitting predictions.
- The form supports both **single-page** and **multi-step** interfaces.
- HTML results are embedded using an `<iframe>` for now (subject to future upgrade to JSON response).

---

## 📂 Folder Structure Overview

```
Deepskin/
├── front/           # React frontend
|   └── deepskin_front
│       └── src/
│           └── components/
│           └── data/
├── deployment/      
|   └── DockerFile   # Backend docker file 
|   └── main.py      # Flask backend
└── models/          
```

<!-- ---

## 📸 Preview

*(Optional: Add a screenshot or screen recording here)* -->

<!-- ---

## 🌐 Live Demo

You can test the deployed version here:  
👉 [https://your-live-demo-link.com](https://your-live-demo-link.com)
``` -->

---

## 🧭 How It Works

1. Select user metadata (sex, age, localization)
2. Upload a clear image of the skin lesion
3. Submit the form
4. Receive a prediction and visual report in an embedded preview

---

## 🧩 Tech Stack

- **Frontend:** React, Axios, HTML/CSS
- **Backend:** Flask (Python), PIL, Docker
- **Deployment:** Local (Dev), Docker (Prod Ready)

---

## 🛡 License

This project is licensed under the MIT License.  
Feel free to use, modify, and distribute it with proper credit.

---

## 🧑‍💻 Authors

This project is developed by a team of 4 passionate contributors:

- **Julien Hansen**
- **Clément Vermeylen**
- **Ramzan Arsanov**
- **Seyfullah Ural**

<!-- 
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify) 
-->

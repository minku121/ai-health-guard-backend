import { Route, Routes } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "@/components/layout";
import IndexPage from "@/pages/index";

function App() {
  return (
    <NextUIProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<IndexPage />} />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </NextUIProvider>
  );
}

export default App;

import { useContext } from "react";
import { Outlet, Navigate } from "react-router-dom";
import { AppContext } from "./AppContext";
import Loading from "./Loading";

export default function PrivateRoute() {
  const { isAuth } = useContext(AppContext);

  if (isAuth === null) return <Loading />;

  return isAuth ? <Outlet /> : <Navigate to="/" />;
}
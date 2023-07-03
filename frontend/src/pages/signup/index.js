import { Container, Input, Title, Main, Form, Button } from "../../components";
import styles from "./styles.module.css";
import { useFormWithValidation } from "../../utils";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../contexts";
import MetaTags from "react-meta-tags";

const SignUp = ({ onSignUp }) => {
  const { values, handleChange, errors, isValid, resetForm } =
    useFormWithValidation();
  const authContext = useContext(AuthContext);

  return (
    <Main>
      {authContext && <Redirect to="/recipes" />}
      <Container>
        <MetaTags>
          <title>Sign Up</title>
          <meta name="description" content="Food companion - Sign Up" />
          <meta property="og:title" content="Sign Up" />
        </MetaTags>
        <Title title="Sign Up" />
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            onSignUp(values);
          }}
        >
          <Input
            label="First Name"
            name="first_name"
            required
            onChange={handleChange}
          />
          <Input
            label="Last Name"
            name="last_name"
            required
            onChange={handleChange}
          />
          <Input
            label="Username"
            name="username"
            required
            onChange={handleChange}
          />

          <Input label="Email" name="email" required onChange={handleChange} />
          <Input
            label="Password"
            type="password"
            name="password"
            required
            onChange={handleChange}
          />
          <Button
            modifier="style_dark-blue"
            type="submit"
            className={styles.button}
            disabled={!isValid}
          >
            Create an account
          </Button>
        </Form>
      </Container>
    </Main>
  );
};

export default SignUp;

import React, { FC, useState } from 'react'
import Form from '../components/Form'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'

const Verify:FC = ()=> {
  
  const navigate = useNavigate()
  
  const [password, setPassword] = useState<string>('')

  const [userName, setUserName] = useState<string>('')

  const [isError, setIsError] = useState<boolean>(false)

  const onChangeName =(e: React.ChangeEvent<HTMLInputElement>)=>{
    setUserName(e.target.value)
  }

  const onChangePassword =(e: React.ChangeEvent<HTMLInputElement>)=>{
    setPassword(e.target.value)
  }

  const onSubmit =(e: React.FormEvent<HTMLFormElement>)=>{
    e.preventDefault()
    fetchVerify(userName, password)
  }

  async function fetchVerify (userName:string, password:string) {
    const response = await PostService.verify(userName, password)

    if (response){
        localStorage.setItem('token', response.token)
        navigate('/')
    }else{
        setIsError(true)
    }
  }
  return (
    <div>
    <h1>Войти</h1>
    <Form password={password} userName={userName} onChangePassword={onChangePassword} onChangeName={onChangeName} onSubmit={onSubmit}/>
    <div>
    Или можете зарегистрироваться
    <button onClick={(e)=>{navigate('/login')}}>Зарегистрироваться</button>
    </div>
    {isError &&
      <div>
          Неверное имя или неверный пароль
      </div>
    }
    </div>

  )
}

export default Verify
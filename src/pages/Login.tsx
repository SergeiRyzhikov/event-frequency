import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import Form from '../components/Form'

const Login:FC = ()=> {
    
    const [userName, setUserName] = useState<string>('')

    const [password, setPassword] = useState<string>('')
    const [errorText, setErrorText] = useState<string>('')

    const onChangeName =(e: React.ChangeEvent<HTMLInputElement>)=>{
        setUserName(e.target.value)
    }
    const onChangePassword =(e: React.ChangeEvent<HTMLInputElement>)=>{
        setPassword(e.target.value)
    }
    const [isError, setIsError] = useState<boolean>(false)


    const navigate = useNavigate()

    async function fetchLogin (userName:string, password:string) {
        
        const response = await PostService.login(userName, password)
        if (response) {
            setIsError(false)
            navigate('/verify')
        }
        else {
            setErrorText('такой пользователь уже существует')
            setIsError(true)
        }
    }
    const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
        e.preventDefault()

        console.log(userName, password)
        if (userName && password.length>=6){
            fetchLogin(userName, password)
        }
        else{
            setErrorText('введите имя пользвателя')
            setIsError(true)
        }
    }
    
    
  return (
    <div>
        <h1>Зарегистрироваться</h1>
        <Form password={password} userName={userName} onChangePassword={onChangePassword} onChangeName={onChangeName} onSubmit={onSubmit}/>
        <div>
            Уже зарегистрировались?
            <button onClick={(e)=>{navigate('/verify')}}>Войти</button>
        </div>
        {isError &&
        <div>
            {errorText}
        </div>
        }
        

    </div>
  )
}

export default Login
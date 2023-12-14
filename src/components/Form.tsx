import { ChangeEventHandler, FC, FormEventHandler } from 'react'

interface IForm {
    onSubmit: FormEventHandler<HTMLFormElement>
    userName: string
    password: string
    onChangeName: ChangeEventHandler<HTMLInputElement>
    onChangePassword: ChangeEventHandler<HTMLInputElement>
}

const Form:FC<IForm> = ({onSubmit, userName, password, onChangeName, onChangePassword}) => {
  return (
    <form onSubmit={onSubmit} className='form'>
        <input type="text" placeholder='Введите имя' value={userName} onChange={onChangeName}/>
        <input type="password" placeholder='Введите пароль' value={password} onChange={onChangePassword} minLength={6}/>
        <button type='submit'>отправить</button>
    </form>
  )
}

export default Form
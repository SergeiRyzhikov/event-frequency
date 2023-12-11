import React, { ChangeEventHandler, FC, FormEventHandler } from 'react'
import { DtPicker } from 'react-calendar-datetime-picker'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'

interface IForm {
    eventName: string
    onChangeEvent: ChangeEventHandler<HTMLInputElement>
    onSubmit: FormEventHandler<HTMLFormElement>
    setDate: React.Dispatch<React.SetStateAction<IDate>> | React.Dispatch<React.SetStateAction<IRangeDate>>
    type: boolean
}

const FormCalendar:FC<IForm> = ({onSubmit, eventName, onChangeEvent, setDate, type}) => {
  return (
    <form action="" onSubmit={onSubmit}>
          <input type="text" placeholder='введите событие' value={eventName} onChange={onChangeEvent}/> 
          {type ?
            <DtPicker  
            onChange={setDate}
            type='range'
            local='en'
            withTime
            isRequired
            showTimeInput
            showWeekend/>
            :
            <DtPicker  
            onChange={setDate}
            type='single'
            local='en'
            withTime
            isRequired
            showTimeInput
            showWeekend/>
          }
          
          <button type='submit' className='send'>отправить</button>
        </form>
  )
}

export default FormCalendar
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${USERNAME}    Admin
${PASSWORD}    admin123

*** Test Cases ***

Đăng Nhập Thành Công
    [Documentation]    Đăng nhập thành công với thông tin hợp lệ
    Open Browser    ${URL}    chrome
    Go To    ${URL}
    Wait Until Element Is Visible    xpath=//input[@name='username']    10s
    Input Text    xpath=//input[@name='username']    ${USERNAME}
    Input Text    xpath=//input[@name='password']    ${PASSWORD}
    TRY
        Click Element    xpath=//button[@type='submit']
    EXCEPT    
        Log    Không tìm thấy nút submit
    END

    Wait Until Element Is Visible    xpath=//span[@class='oxd-userdropdown-name']    15s
    ${status}    ${message}=    Run Keyword And Ignore Error    Page Should Contain Element    xpath=//span[@class='oxd-userdropdown-name']
    IF           '${status}' == 'PASS'
                 Log    Successfully logged into the application
    ELSE
                 Log    Please verify userid and password
    END
    Page Should Contain Element    xpath=//span[@class='oxd-userdropdown-name']
    Log To Console    Successfully logged into the application
    Close Browser

Đăng Nhập Không Thành Công
    [Documentation]    Đăng nhập không thành công với thông tin không hợp lệ
    Open Browser    ${URL}    chrome
    Go To    ${URL}
    Wait Until Element Is Visible    xpath=//input[@name='username']    10s
    Input Text    xpath=//input[@name='username']    123456
    Input Text    xpath=//input[@name='password']    123456
    TRY
        Click Element    xpath=//button[@type='submit']
    EXCEPT    
        Log    Không tìm thấy nút submit
    END

    ${status}    ${message}=    Run Keyword And Ignore Error    Page Should Contain    Welcome
    IF           '${status}' == 'Welcome'
                 Log    Successfully logged into the application
    ELSE
                 Log    Please verify userid and password
    END

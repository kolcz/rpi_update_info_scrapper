if ($args.Count -gt 0) {
    $cwd = (Get-Location).ToString()
    $template = [Windows.UI.Notifications.ToastTemplateType, Windows.UI.Notifications, ContentType = WindowsRuntime]::ToastImageAndText01
    $TemplateContent = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::GetTemplateContent($template)
    $TemplateContent.SelectSingleNode('//text[@id="1"]').InnerText = $args[0]
    $TemplateContent.SelectSingleNode('//image[@id="1"]').setAttribute("src", $cwd + "\notification_image.png")
    
    $title = 'RPi Update Scrapper'
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($title).Show($TemplateContent)
}
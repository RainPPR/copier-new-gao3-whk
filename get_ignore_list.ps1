# 获取当前工作目录的路径
$currentDir = (Get-Location).Path

# 获取所有文件并转换为相对路径
Get-ChildItem -File -Recurse | ForEach-Object {
    # 移除绝对路径中的当前目录部分
    $relativePath = $_.FullName.Replace($currentDir, "").TrimStart([System.IO.Path]::DirectorySeparatorChar)
    # 将 Windows 路径分隔符 \ 替换为 /
    $relativePath.Replace('\', '/')
}

#!/bin/bash

# Quality Problem Expert Skill - 自动部署脚本
# 用于本地开发后快速部署到GitHub

set -e

echo "=================================================="
echo "Quality Problem Expert Skill - 自动部署脚本"
echo "=================================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# 检查Git状态
check_git_status() {
    print_message $BLUE "检查Git状态..."

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_message $RED "错误: 当前目录不是Git仓库"
        exit 1
    fi

    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        print_message $YELLOW "警告: 有未提交的更改"
        git status --porcelain
        echo ""

        read -p "是否要继续? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_message $YELLOW "部署已取消"
            exit 1
        fi
    fi

    print_message $GREEN "✅ Git状态检查通过"
}

# 验证Skill结构
validate_skill_structure() {
    print_message $BLUE "验证Skill结构..."

    local errors=0

    # 检查必需文件
    if [ ! -f "SKILL.md" ]; then
        print_message $RED "❌ 缺少SKILL.md文件"
        errors=$((errors + 1))
    fi

    # 检查必需目录
    for dir in scripts references assets; do
        if [ ! -d "$dir" ]; then
            print_message $RED "❌ 缺少$dir目录"
            errors=$((errors + 1))
        fi
    done

    # 检查Python脚本语法
    if [ -d "scripts" ]; then
        for script in scripts/*.py; do
            if [ -f "$script" ]; then
                if python -m py_compile "$script" 2>/dev/null; then
                    print_message $GREEN "✅ $script 语法检查通过"
                else
                    print_message $RED "❌ $script 语法错误"
                    errors=$((errors + 1))
                fi
            fi
        done
    fi

    if [ $errors -eq 0 ]; then
        print_message $GREEN "✅ Skill结构验证通过"
    else
        print_message $RED "❌ 发现$errors个错误，请修复后再试"
        exit 1
    fi
}

# 自动生成提交信息
generate_commit_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local branch=$(git branch --show-current)

    # 检测更改的文件类型
    local changes=$(git diff --cached --name-only)

    if echo "$changes" | grep -q "^scripts/"; then
        echo "feat: Update skill scripts - $timestamp"
    elif echo "$changes" | grep -q "^references/"; then
        echo "docs: Update references - $timestamp"
    elif echo "$changes" | grep -q "^assets/"; then
        echo "style: Update assets/templates - $timestamp"
    elif echo "$changes" | grep -q "SKILL.md"; then
        echo "feat: Update skill definition - $timestamp"
    else
        echo "chore: Update skill components - $timestamp"
    fi
}

# 创建包文件
create_package() {
    print_message $BLUE "创建Skill包文件..."

    if command -v zip >/dev/null 2>&1; then
        zip -r quality-problem-expert.zip . -x ".git/*" "*.log" "__pycache__/*" "*.pyc" >/dev/null 2>&1
        if [ -f "quality-problem-expert.zip" ]; then
            print_message $GREEN "✅ 包文件创建成功: quality-problem-expert.zip"
        else
            print_message $YELLOW "⚠️ 包文件创建失败"
        fi
    else
        print_message $YELLOW "⚠️ zip命令未找到，跳过包文件创建"
    fi
}

# 主部署流程
main() {
    echo ""
    print_message $GREEN "开始部署流程..."
    echo ""

    # 步骤1: 检查Git状态
    check_git_status
    echo ""

    # 步骤2: 验证Skill结构
    validate_skill_structure
    echo ""

    # 步骤3: 添加更改
    print_message $BLUE "添加文件到Git..."
    git add scripts/ references/ assets/ SKILL.md README.md AUTOMATION.md 2>/dev/null || git add .

    # 检查是否有更改
    if git diff --cached --quiet; then
        print_message $YELLOW "没有更改需要提交"
    else
        # 步骤4: 生成提交信息
        local commit_msg=$(generate_commit_message)
        echo ""
        print_message $BLUE "提交信息: $commit_msg"

        # 步骤5: 提交
        git commit -m "$commit_msg"
        print_message $GREEN "✅ 提交完成"

        # 步骤6: 推送到GitHub
        print_message $BLUE "推送到GitHub..."
        if git push origin main; then
            print_message $GREEN "✅ 推送到GitHub成功"
            print_message $GREEN "🌐 GitHub Actions将自动处理部署"
        else
            print_message $RED "❌ 推送到GitHub失败"
            exit 1
        fi
    fi

    echo ""

    # 步骤7: 创建包文件
    create_package
    echo ""

    # 完成
    print_message $GREEN "=================================================="
    print_message $GREEN "部署完成!"
    print_message $GREEN "=================================================="
    print_message $BLUE "📊 查看状态: https://github.com/yhai3596/quality-assisant/actions"
    print_message $BLUE "📦 查看代码: https://github.com/yhai3596/quality-assisant"
    echo ""
}

# 显示帮助信息
show_help() {
    echo "Quality Problem Expert Skill - 自动部署脚本"
    echo ""
    echo "用法:"
    echo "  ./deploy.sh [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help      显示帮助信息"
    echo "  -v, --validate  仅验证Skill结构"
    echo "  -p, --package   仅创建包文件"
    echo ""
    echo "示例:"
    echo "  ./deploy.sh              # 执行完整部署"
    echo "  ./deploy.sh --validate   # 仅验证结构"
    echo "  ./deploy.sh --package   # 仅创建包"
}

# 解析命令行参数
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -v|--validate)
        validate_skill_structure
        exit 0
        ;;
    -p|--package)
        create_package
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_message $RED "未知选项: $1"
        show_help
        exit 1
        ;;
esac
